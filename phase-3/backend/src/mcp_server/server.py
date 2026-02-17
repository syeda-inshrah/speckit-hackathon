"""MCP Server for Todo Task Operations using Official MCP SDK"""
import json
from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.database import get_session
from src.models.task import Task

# MCP SDK imports - optional for web deployment
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
    # Initialize MCP Server (for tool registration only in web deployment)
    app = Server("todo-mcp-server")
except ImportError:
    MCP_AVAILABLE = False
    app = None
    Tool = None
    TextContent = None
    print("MCP SDK not available - using direct function calls")


# Only register MCP decorators if SDK is available
if MCP_AVAILABLE:
    @app.list_tools()
    async def list_tools() -> list[Tool]:
        """List all available MCP tools"""
        return [
            Tool(
                name="add_task",
            description="Create a new task for the user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the user creating the task"
                    },
                    "title": {
                        "type": "string",
                        "description": "The title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the task"
                    }
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List all tasks for a user, optionally filtered by completion status",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the user"
                    },
                    "completed": {
                        "type": ["boolean", "null"],
                        "description": "Filter by completion status: true for completed, false for incomplete, null for all"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the user"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to complete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update a task's title or description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the user"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "Optional new title for the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional new description for the task"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the user"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        )
    ]


    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Execute a tool by name with given arguments"""

        # Get database session
        async for session in get_session():
            try:
                if name == "add_task":
                    result = await _add_task(
                        session=session,
                        user_id=arguments["user_id"],
                        title=arguments["title"],
                        description=arguments.get("description")
                    )
                elif name == "list_tasks":
                    result = await _list_tasks(
                        session=session,
                        user_id=arguments["user_id"],
                        completed=arguments.get("completed")
                    )
                elif name == "complete_task":
                    result = await _complete_task(
                        session=session,
                        user_id=arguments["user_id"],
                        task_id=arguments["task_id"]
                    )
                elif name == "update_task":
                    result = await _update_task(
                        session=session,
                        user_id=arguments["user_id"],
                        task_id=arguments["task_id"],
                        title=arguments.get("title"),
                        description=arguments.get("description")
                    )
                elif name == "delete_task":
                    result = await _delete_task(
                        session=session,
                        user_id=arguments["user_id"],
                        task_id=arguments["task_id"]
                    )
                else:
                    result = {
                        "success": False,
                        "message": f"Unknown tool: {name}"
                    }

                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]

            finally:
                await session.close()


# Tool Implementation Functions

async def _add_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> dict:
    """Create a new task"""
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
            "task_id": new_task.id,
            "title": new_task.title
        }
    except Exception as e:
        await session.rollback()
        return {
            "success": False,
            "message": f"Error creating task: {str(e)}",
            "task_id": None
        }


async def _list_tasks(
    session: AsyncSession,
    user_id: str,
    completed: Optional[bool] = None
) -> dict:
    """List all tasks for a user"""
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


async def _complete_task(
    session: AsyncSession,
    user_id: str,
    task_id: int
) -> dict:
    """Mark a task as completed"""
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
            "task_id": task.id,
            "title": task.title
        }
    except Exception as e:
        await session.rollback()
        return {
            "success": False,
            "message": f"Error completing task: {str(e)}",
            "task_id": task_id
        }


async def _update_task(
    session: AsyncSession,
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """Update a task's title or description"""
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
            "task_id": task.id,
            "title": task.title
        }
    except Exception as e:
        await session.rollback()
        return {
            "success": False,
            "message": f"Error updating task: {str(e)}",
            "task_id": task_id
        }


async def _delete_task(
    session: AsyncSession,
    user_id: str,
    task_id: int
) -> dict:
    """Delete a task"""
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

        task_title = task.title
        await session.delete(task)
        await session.commit()

        return {
            "success": True,
            "message": f"Deleted task: {task_title}",
            "task_id": task_id
        }
    except Exception as e:
        await session.rollback()
        return {
            "success": False,
            "message": f"Error deleting task: {str(e)}",
            "task_id": task_id
        }


# Commented out for web deployment - MCP tools are called directly as functions
# async def main():
#     """Run the MCP server"""
#     async with stdio_server() as (read_stream, write_stream):
#         await app.run(
#             read_stream,
#             write_stream,
#             app.create_initialization_options()
#         )


# if __name__ == "__main__":
#     asyncio.run(main())
