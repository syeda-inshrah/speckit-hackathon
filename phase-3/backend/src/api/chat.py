"""Chat API endpoints for AI-powered task management with Groq + MCP"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from typing import List

from src.core.database import get_session
from src.middleware.auth import get_current_user, verify_user_access
from src.models.user import User
# Use Groq agent with MCP tool integration
from src.core.groq_mcp_agent import groq_mcp_agent
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

router = APIRouter(prefix="", tags=["chat"])


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: UUID,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Send a chat message and get AI response using OpenAI Agents SDK with MCP tools
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

        # Run agent with Groq + MCP tools
        agent_response = await groq_mcp_agent.run_agent(
            user_message=request.message,
            conversation_history=history,
            user_id=user_id,
            session=session
        )

        # Extract task operations from MCP tool results
        task_operations = []
        if agent_response.get("tool_results"):
            for tool_exec in agent_response["tool_results"]:
                tool_name = tool_exec.get("tool", "")
                result = tool_exec.get("result", {})

                if result.get("success"):
                    task_operations.append(TaskOperation(
                        operation=tool_name,
                        task_id=result.get("task_id"),
                        title=result.get("title"),
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
