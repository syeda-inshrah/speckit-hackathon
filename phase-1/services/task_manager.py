"""Task manager service for in-memory task storage and operations.

Provides CRUD operations and validation for todo tasks in an in-memory list.
"""

from typing import List, Optional
from datetime import datetime


class TaskManager:
    """Manages in-memory storage and operations for todo tasks."""

    def __init__(self) -> None:
        """Initialize task manager with empty task list and ID counter."""
        self._tasks: List[dict] = []
        self._next_id: int = 1

    def add_task(
        self,
        title: str,
        description: Optional[str] = None
    ) -> dict:
        """
        Add a new task to the in-memory task list.

        Args:
            title: Task title (required, 1-200 characters, non-empty)
            description: Optional task description (max 1000 characters)

        Returns:
            dict with task object and status

        Raises:
            ValueError: If title is invalid
        """
        # Validate title
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title.strip()) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        if description is not None and len(description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")

        # Create task object
        task_id = self._next_id
        task = {
            "id": task_id,
            "title": title.strip(),
            "description": description.strip() if description else None,
            "completed": False,
            "created_at": datetime.now()
        }

        # Add to storage
        self._tasks.append(task)
        self._next_id += 1

        return {
            "status": "success",
            "task": task,
            "message": f"Task {task_id} created successfully"
        }

    def get_task(self, task_id: int) -> Optional[dict]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: Task identifier

        Returns:
            Task dict if found, None otherwise
        """
        for task in self._tasks:
            if task["id"] == task_id:
                return task
        return None

    def get_all_tasks(self) -> List[dict]:
        """
        Retrieve all tasks from in-memory storage.

        Returns:
            List of all task dictionaries
        """
        return self._tasks

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> dict:
        """
        Update an existing task's title and/or description.

        Args:
            task_id: Task identifier to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            dict with status and updated task

        Raises:
            ValueError: If task_id is invalid or inputs are invalid
        """
        # Validate task exists
        task = self.get_task(task_id)
        if task is None:
            raise ValueError("Task not found")

        # Update fields
        updates = {}
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty")
            if len(title.strip()) > 200:
                raise ValueError("Title cannot exceed 200 characters")
            task["title"] = title.strip()
            updates["title"] = True

        if description is not None:
            if len(description) > 1000:
                raise ValueError("Description cannot exceed 1000 characters")
            task["description"] = description.strip() if description else None
            updates["description"] = True

        return {
            "status": "success",
            "task": task,
            "message": f"Task {task_id} updated successfully",
            "updates": list(updates.keys())
        }

    def delete_task(self, task_id: int) -> dict:
        """
        Delete a task from the in-memory task list.

        Args:
            task_id: Task identifier to delete

        Returns:
            dict with status and message
        """
        # Validate task exists
        task = self.get_task(task_id)
        if task is None:
            raise ValueError("Task not found")

        # Remove from storage
        self._tasks.remove(task)

        return {
            "status": "success",
            "message": f"Task {task_id} deleted successfully"
        }

    def toggle_complete(self, task_id: int) -> dict:
        """
        Toggle the completion status of a task.

        Args:
            task_id: Task identifier to toggle

        Returns:
            dict with status, updated task, and message
        """
        # Validate task exists
        task = self.get_task(task_id)
        if task is None:
            raise ValueError("Task not found")

        # Toggle status
        task["completed"] = not task["completed"]

        return {
            "status": "success",
            "task": task,
            "message": f"Task {task_id} {'completed' if task['completed'] else 'marked incomplete'}"
        }

    def task_exists(self, task_id: int) -> bool:
        """
        Check if a task exists in the task list.

        Args:
            task_id: Task identifier to check

        Returns:
            True if task exists, False otherwise
        """
        return self.get_task(task_id) is not None
