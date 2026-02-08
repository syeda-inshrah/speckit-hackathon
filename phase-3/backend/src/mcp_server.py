"""MCP Server for Task Operations using FastMCP"""
from typing import Any, Optional
from mcp.server.fastmcp import FastMCP
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from uuid import UUID
from datetime import datetime

from src.models.task import Task
from src.core.config import settings

# Initialize FastMCP server
mcp = FastMCP("todo-tasks")

# Database setup - will be initialized when needed
engine = None
async_session_maker = None


def init_database():
    """Initialize database engine and session maker"""
    global engine, async_session_maker

    if engine is None:
        # Ensure URL uses asyncpg driver
        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        engine = create_async_engine(
            db_url,
            echo=False,
            future=True
        )

        async_session_maker = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )


async def get_db_session() -> AsyncSession:
    """Get database session"""
    async with async_session_maker() as session:
        return session


@mcp.tool()
async def add_task(
    user_id: str,
    title: str,
    description: str = None
) -> dict[str, Any]:
    """Create a new task for the user.

    Args:
        user_id: The UUID of the user creating the task
        title: The title of the task
        description: Optional description of the task

    Returns:
        Dictionary with success status, message, and task_id
    """
    try:
        init_database()
        async with async_session_maker() as session:
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


@mcp.tool()
async def list_tasks(
    user_id: str,
    completed: Optional[bool] = None
) -> dict[str, Any]:
    """List all tasks for a user, optionally filtered by completion status.

    Args:
        user_id: The UUID of the user
        completed: Optional filter - true for completed, false for incomplete, null for all

    Returns:
        Dictionary with success status, message, and list of tasks
    """
    try:
        init_database()
        async with async_session_maker() as session:
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


@mcp.tool()
async def complete_task(
    user_id: str,
    task_id: int
) -> dict[str, Any]:
    """Mark a task as completed.

    Args:
        user_id: The UUID of the user
        task_id: The ID of the task to complete

    Returns:
        Dictionary with success status and message
    """
    try:
        init_database()
        async with async_session_maker() as session:
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


@mcp.tool()
async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict[str, Any]:
    """Update a task's title or description.

    Args:
        user_id: The UUID of the user
        task_id: The ID of the task to update
        title: Optional new title for the task
        description: Optional new description for the task

    Returns:
        Dictionary with success status and message
    """
    try:
        init_database()
        async with async_session_maker() as session:
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


@mcp.tool()
async def delete_task(
    user_id: str,
    task_id: int
) -> dict[str, Any]:
    """Delete a task.

    Args:
        user_id: The UUID of the user
        task_id: The ID of the task to delete

    Returns:
        Dictionary with success status and message
    """
    try:
        init_database()
        async with async_session_maker() as session:
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


def main():
    """Run the MCP server"""
    # Run with stdio transport
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
