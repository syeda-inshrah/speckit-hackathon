"""Task entity model for console todo application."""

from datetime import datetime
from typing import Optional


class Task:
    """Represents a single todo item with all required attributes."""

    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime

    def __init__(
        self,
        id: int,
        title: str,
        description: Optional[str] = None,
        completed: bool = False,
        created_at: Optional[datetime] = None
    ) -> None:
        """
        Initialize a new Task instance.

        Args:
            id: Unique sequential identifier for this task
            title: Task title (1-200 characters, non-empty)
            description: Optional task description (up to 1000 characters)
            completed: Task completion status (default False)
            created_at: Optional creation timestamp (defaults to now)
        """
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now()
