from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.task import Task
    from src.models.conversation import Conversation


class User(SQLModel, table=True):
    """User model for authentication and task ownership"""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)
    conversations: list["Conversation"] = Relationship(back_populates="user", cascade_delete=True)
