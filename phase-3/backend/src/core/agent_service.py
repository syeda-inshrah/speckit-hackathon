"""OpenAI Agents SDK service layer with function tools"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from agents import Agent, Runner, function_tool
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import settings
from src.models.task import Task


# Define MCP-style tools using function_tool decorator
@function_tool
async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> dict:
    """Create a new task for the user.

    Args:
        user_id: The UUID of the user creating the task
        title: The title of the task
        description: Optional description of the task

    Returns:
        Dictionary with success status, message, and task_id
    """
    # Access session from context (injected by Runner)
    from agents import tool_context
    context = tool_context.get()
    session = context.get("session")

    try:
        new_task = Task(
            user_id=UUID(user_id),
            title=title,
            description=description,
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
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating task: {str(e)}",
            "task_id": None
        }


@function_tool
async def list_tasks(
    user_id: str,
    completed: Optional[bool] = None
) -> dict:
    """List all tasks for a user, optionally filtered by completion status.

    Args:
        user_id: The UUID of the user
        completed: Optional filter - true for completed, false for incomplete, null for all

    Returns:
        Dictionary with success status, message, and list of tasks
    """
    # Access session from context
    from agents import tool_context
    context = tool_context.get()
    session = context.get("session")

    try:
        query = select(Task).where(Task.user_id == UUID(user_id))

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
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None
            }
            for task in tasks
        ]

        return {
            "success": True,
            "message": f"Found {len(tasks)} task(s)",
            "tasks": task_list
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error listing tasks: {str(e)}",
            "tasks": []
        }


@function_tool
async def complete_task(
    user_id: str,
    task_id: int
) -> dict:
    """Mark a task as completed.

    Args:
        user_id: The UUID of the user
        task_id: The ID of the task to complete

    Returns:
        Dictionary with success status and message
    """
    # Access session from context
    from agents import tool_context
    context = tool_context.get()
    session = context.get("session")

    try:
        result = await session.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == UUID(user_id)
            )
        )
        task = result.scalar_one_or_none()

        if not task:
            return {
                "success": False,
                "message": f"Task {task_id} not found",
                "task_id": task_id
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
    except Exception as e:
        return {
            "success": False,
            "message": f"Error completing task: {str(e)}",
            "task_id": task_id
        }


@function_tool
async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """Update a task's title or description.

    Args:
        user_id: The UUID of the user
        task_id: The ID of the task to update
        title: Optional new title for the task
        description: Optional new description for the task

    Returns:
        Dictionary with success status and message
    """
    # Access session from context
    from agents import tool_context
    context = tool_context.get()
    session = context.get("session")

    try:
        result = await session.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == UUID(user_id)
            )
        )
        task = result.scalar_one_or_none()

        if not task:
            return {
                "success": False,
                "message": f"Task {task_id} not found",
                "task_id": task_id
            }

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        task.updated_at = datetime.utcnow()
        session.add(task)
        await session.commit()

        return {
            "success": True,
            "message": f"Updated task: {task.title}",
            "task_id": task.id
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating task: {str(e)}",
            "task_id": task_id
        }


@function_tool
async def delete_task(
    user_id: str,
    task_id: int
) -> dict:
    """Delete a task.

    Args:
        user_id: The UUID of the user
        task_id: The ID of the task to delete

    Returns:
        Dictionary with success status and message
    """
    # Access session from context
    from agents import tool_context
    context = tool_context.get()
    session = context.get("session")

    try:
        result = await session.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == UUID(user_id)
            )
        )
        task = result.scalar_one_or_none()

        if not task:
            return {
                "success": False,
                "message": f"Task {task_id} not found",
                "task_id": task_id
            }

        await session.delete(task)
        await session.commit()

        return {
            "success": True,
            "message": f"Deleted task {task_id}",
            "task_id": task_id
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error deleting task: {str(e)}",
            "task_id": task_id
        }


class AgentServiceWithTools:
    """Service for managing OpenAI Agents SDK with function tools"""

    def __init__(self):
        self.agent_name = settings.AGENT_NAME
        self.agent_instructions = settings.AGENT_INSTRUCTIONS
        self.model = settings.OPENROUTER_MODEL
        self.agent = None

    def _initialize_agent(self):
        """Initialize the agent with instructions and tools"""
        if self.agent is None:
            # Set OpenAI API key for OpenRouter
            import os
            os.environ["OPENAI_API_KEY"] = settings.OPENROUTER_API_KEY
            os.environ["OPENAI_BASE_URL"] = settings.OPENROUTER_BASE_URL

            # Create the agent with function tools
            self.agent = Agent(
                name=self.agent_name,
                instructions=self.agent_instructions,
                model=self.model,
                tools=[add_task, list_tasks, complete_task, update_task, delete_task]
            )

    async def run_agent(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_id: UUID,
        session: AsyncSession,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run the agent with OpenAI Agents SDK and function tools

        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            user_id: The user's UUID (passed to tools)
            session: Database session for tool execution
            context: Optional context dictionary

        Returns:
            Dictionary containing the response and tool execution results
        """
        try:
            # Ensure agent is initialized
            self._initialize_agent()

            # Prepare context with user_id and session for tools
            agent_context = context or {}
            agent_context["user_id"] = str(user_id)
            agent_context["session"] = session

            # Build the conversation messages
            messages = []
            for msg in conversation_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            # Add the current user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Run the agent with Runner
            result = await Runner.run(
                starting_agent=self.agent,
                input=messages,
                context=agent_context
            )

            # Extract response from Result
            response_data = {
                "content": "",
                "tool_calls": [],
                "tool_results": []
            }

            # Get the final output
            if hasattr(result, "final_output"):
                response_data["content"] = result.final_output
            elif hasattr(result, "output"):
                response_data["content"] = result.output

            # Extract tool calls from result items
            if hasattr(result, "items"):
                for item in result.items:
                    # Check if this is a tool call item
                    if hasattr(item, "tool_name"):
                        response_data["tool_calls"].append({
                            "function": {
                                "name": item.tool_name,
                                "arguments": getattr(item, "tool_input", {})
                            }
                        })

                        # Check if there's a tool result
                        if hasattr(item, "tool_output"):
                            response_data["tool_results"].append({
                                "result": item.tool_output
                            })

            return response_data

        except Exception as e:
            raise Exception(f"Agent execution error: {str(e)}")


# Singleton instance
agent_service_mcp = AgentServiceWithTools()
