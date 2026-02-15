from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID
from datetime import datetime
from src.core.database import get_session
from src.middleware.auth import get_current_user, verify_user_access
from src.models.user import User
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/{user_id}/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[TaskResponse]:
    """
    List all tasks for the authenticated user.

    - Verifies user_id matches authenticated user
    - Returns tasks ordered by creation date (newest first)
    """
    # Verify user has access to this resource
    verify_user_access(current_user, user_id)

    # Fetch all tasks for the user
    result = await session.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()

    return [TaskResponse.model_validate(task) for task in tasks]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: UUID,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    - Verifies user_id matches authenticated user
    - Title is required (1-200 characters)
    - Description is optional (max 1000 characters)
    """
    # Verify user has access to this resource
    verify_user_access(current_user, user_id)

    # Create new task
    new_task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
    )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return TaskResponse.model_validate(new_task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: UUID,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Get a specific task by ID.

    - Verifies user_id matches authenticated user
    - Returns 404 if task not found or doesn't belong to user
    """
    # Verify user has access to this resource
    verify_user_access(current_user, user_id)

    # Fetch task
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: UUID,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Update a task's title and/or description.

    - Verifies user_id matches authenticated user
    - Returns 404 if task not found or doesn't belong to user
    """
    # Verify user has access to this resource
    verify_user_access(current_user, user_id)

    # Fetch task
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update task fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description

    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return TaskResponse.model_validate(task)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(
    user_id: UUID,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Toggle task completion status.

    - Verifies user_id matches authenticated user
    - Returns 404 if task not found or doesn't belong to user
    """
    # Verify user has access to this resource
    verify_user_access(current_user, user_id)

    # Fetch task
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: UUID,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete a task permanently.

    - Verifies user_id matches authenticated user
    - Returns 404 if task not found or doesn't belong to user
    """
    # Verify user has access to this resource
    verify_user_access(current_user, user_id)

    # Fetch task
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Delete task
    await session.delete(task)
    await session.commit()
