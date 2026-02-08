from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class MessageBase(BaseModel):
    """Base schema for messages"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class MessageCreate(MessageBase):
    """Schema for creating a message"""
    conversation_id: int


class MessageResponse(MessageBase):
    """Schema for message response"""
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    """Base schema for conversations"""
    title: Optional[str] = Field(None, max_length=200)


class ConversationCreate(ConversationBase):
    """Schema for creating a conversation"""
    pass


class ConversationResponse(ConversationBase):
    """Schema for conversation response"""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = None

    class Config:
        from_attributes = True


class ConversationDetail(ConversationResponse):
    """Schema for detailed conversation with messages"""
    messages: List[MessageResponse] = []


class ChatRequest(BaseModel):
    """Schema for chat request"""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    conversation_id: Optional[int] = Field(None, description="Existing conversation ID (optional)")


class TaskOperation(BaseModel):
    """Schema for task operations performed by AI"""
    operation: str = Field(..., description="Operation type: add, list, complete, update, delete")
    task_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    details: Optional[str] = None


class ChatResponse(BaseModel):
    """Schema for chat response"""
    conversation_id: int
    message: MessageResponse
    task_operations: List[TaskOperation] = Field(default_factory=list, description="Task operations performed")
