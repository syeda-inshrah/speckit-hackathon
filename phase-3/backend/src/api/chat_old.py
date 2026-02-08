"""Chat API endpoints for AI-powered task management"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from typing import List
from datetime import datetime

from src.core.database import get_session
from src.middleware.auth import get_current_user, verify_user_access
from src.models.user import User
from src.core.agent_service import agent_service
from src.core.conversation_service import ConversationService, MessageService
from src.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationResponse,
    ConversationDetail,
    MessageCreate,
    MessageResponse,
    TaskOperation,
    ConversationCreate
)
from src.schemas.task import TaskCreate, TaskUpdate
from src.models.task import Task
from sqlmodel import select

router = APIRouter(prefix="/api", tags=["chat"])


class MCPToolsService:
    """Service for executing MCP tool operations"""

    @staticmethod
    async def execute_tool(
        tool_name: str,
        arguments: dict,
        user_id: UUID,
        session: AsyncSession
    ) -> dict:
        """Execute a tool operation and return the result"""

        if tool_name == "add_task":
            # Create a new task
            new_task = Task(
                user_id=user_id,
                title=arguments["title"],
                description=arguments.get("description"),
                completed=False
            )
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)

            return {
                "success": True,
                "message": f"Created task: {new_task.title}",
                "task_id": new_task.id
            }

        elif tool_name == "list_tasks":
            # List tasks
            completed = arguments.get("completed")

            query = select(Task).where(Task.user_id == user_id)
            if completed is not None:
                query = query.where(Task.completed == completed)
            query = query.order_by(Task.created_at.desc())

            result = await session.execute(query)
            tasks = result.scalars().all()

            if not tasks:
                return {
                    "success": True,
                    "message": "No tasks found",
                    "tasks": []
                }

            task_list = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
                for task in tasks
            ]

            return {
                "success": True,
                "message": f"Found {len(tasks)} task(s)",
                "tasks": task_list
            }

        elif tool_name == "complete_task":
            # Complete a task
            task_id = arguments["task_id"]

            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()

            if not task:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found"
                }

            task.completed = True
            task.updated_at = datetime.utcnow()
            session.add(task)
            await session.commit()

            return {
                "success": True,
                "message": f"Completed task: {task.title}",
                "task_id": task.id
            }

        elif tool_name == "update_task":
            # Update a task
            task_id = arguments["task_id"]

            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()

            if not task:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found"
                }

            if "title" in arguments:
                task.title = arguments["title"]
            if "description" in arguments:
                task.description = arguments["description"]

            task.updated_at = datetime.utcnow()
            session.add(task)
            await session.commit()

            return {
                "success": True,
                "message": f"Updated task: {task.title}",
                "task_id": task.id
            }

        elif tool_name == "delete_task":
            # Delete a task
            task_id = arguments["task_id"]

            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()

            if not task:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found"
                }

            await session.delete(task)
            await session.commit()

            return {
                "success": True,
                "message": f"Deleted task {task_id}",
                "task_id": task_id
            }

        else:
            return {
                "success": False,
                "message": f"Unknown tool: {tool_name}"
            }


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: UUID,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Send a chat message and get AI response with task operations using OpenAI Agents SDK
    """
    # Verify user authorization
    verify_user_access(current_user, user_id)

    try:
        # Get or create conversation
        if request.conversation_id:
            conversation = await ConversationService.get_conversation(
                session, request.conversation_id, user_id
            )
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
        else:
            # Create new conversation
            conversation = await ConversationService.create_conversation(
                session,
                user_id,
                ConversationCreate(title=request.message[:50])
            )

        # Get conversation history
        history = await MessageService.get_conversation_history(session, conversation.id)

        # Save user message
        user_message = await MessageService.create_message(
            session,
            MessageCreate(
                conversation_id=conversation.id,
                role="user",
                content=request.message
            )
        )

        # Prepare messages for agent
        messages = history + [{
            "role": "user",
            "content": request.message
        }]

        # Create tool executor function
        async def tool_executor(function_name: str, arguments: dict):
            return await MCPToolsService.execute_tool(
                function_name,
                arguments,
                user_id,
                session
            )

        # Run agent with tools
        agent_response = await agent_service.run_with_tools(messages, tool_executor)

        # Extract task operations from tool results
        task_operations = []
        if agent_response.get("tool_calls"):
            for tool_call, tool_result in zip(
                agent_response["tool_calls"],
                agent_response.get("tool_results", [])
            ):
                function_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]
                result = tool_result["result"]

                task_operations.append(TaskOperation(
                    operation=function_name,
                    task_id=result.get("task_id"),
                    title=arguments.get("title"),
                    description=arguments.get("description"),
                    details=result.get("message")
                ))

        # Save assistant message
        assistant_content = agent_response.get("content", "")
        assistant_message = await MessageService.create_message(
            session,
            MessageCreate(
                conversation_id=conversation.id,
                role="assistant",
                content=assistant_content
            )
        )

        # Update conversation timestamp
        await ConversationService.update_conversation_timestamp(session, conversation.id)

        return ChatResponse(
            conversation_id=conversation.id,
            message=MessageResponse(
                id=assistant_message.id,
                conversation_id=assistant_message.conversation_id,
                role=assistant_message.role,
                content=assistant_message.content,
                created_at=assistant_message.created_at
            ),
            task_operations=task_operations
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}"
        )


@router.get("/{user_id}/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    user_id: UUID,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get all conversations for a user"""
    verify_user_access(current_user, user_id)

    conversations = await ConversationService.get_conversations(session, user_id, skip, limit)

    # Add message count to each conversation
    result = []
    for conv in conversations:
        messages = await MessageService.get_messages(session, conv.id)
        result.append(ConversationResponse(
            id=conv.id,
            user_id=str(conv.user_id),
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=len(messages)
        ))

    return result


@router.get("/{user_id}/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    user_id: UUID,
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific conversation with all messages"""
    verify_user_access(current_user, user_id)

    conversation = await ConversationService.get_conversation(session, conversation_id, user_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    messages = await MessageService.get_messages(session, conversation_id)

    return ConversationDetail(
        id=conversation.id,
        user_id=str(conversation.user_id),
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[
            MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in messages
        ]
    )


@router.delete("/{user_id}/conversations/{conversation_id}")
async def delete_conversation(
    user_id: UUID,
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a conversation"""
    verify_user_access(current_user, user_id)

    success = await ConversationService.delete_conversation(session, conversation_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return {"message": "Conversation deleted successfully"}
