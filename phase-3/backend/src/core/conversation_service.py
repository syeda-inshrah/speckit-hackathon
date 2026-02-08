"""Service layer for conversation and message operations"""
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from src.models.conversation import Conversation
from src.models.message import Message
from src.schemas.chat import (
    ConversationCreate,
    ConversationResponse,
    ConversationDetail,
    MessageCreate,
    MessageResponse
)


class ConversationService:
    """Service for conversation operations"""

    @staticmethod
    async def create_conversation(
        session: AsyncSession,
        user_id: UUID,
        conversation_data: ConversationCreate
    ) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(
            user_id=user_id,
            title=conversation_data.title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        return conversation

    @staticmethod
    async def get_conversation(
        session: AsyncSession,
        conversation_id: int,
        user_id: UUID
    ) -> Optional[Conversation]:
        """Get a conversation by ID"""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_conversations(
        session: AsyncSession,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> List[Conversation]:
        """Get all conversations for a user"""
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(statement)
        return list(result.scalars().all())

    @staticmethod
    async def update_conversation_timestamp(
        session: AsyncSession,
        conversation_id: int
    ) -> None:
        """Update conversation's updated_at timestamp"""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        result = await session.execute(statement)
        conversation = result.scalar_one_or_none()
        if conversation:
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            await session.commit()

    @staticmethod
    async def delete_conversation(
        session: AsyncSession,
        conversation_id: int,
        user_id: UUID
    ) -> bool:
        """Delete a conversation"""
        conversation = await ConversationService.get_conversation(session, conversation_id, user_id)
        if conversation:
            await session.delete(conversation)
            await session.commit()
            return True
        return False


class MessageService:
    """Service for message operations"""

    @staticmethod
    async def create_message(
        session: AsyncSession,
        message_data: MessageCreate
    ) -> Message:
        """Create a new message"""
        message = Message(
            conversation_id=message_data.conversation_id,
            role=message_data.role,
            content=message_data.content,
            created_at=datetime.utcnow()
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message

    @staticmethod
    async def get_messages(
        session: AsyncSession,
        conversation_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Message]:
        """Get all messages for a conversation"""
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(statement)
        return list(result.scalars().all())

    @staticmethod
    async def get_conversation_history(
        session: AsyncSession,
        conversation_id: int
    ) -> List[dict]:
        """Get conversation history formatted for OpenAI API"""
        messages = await MessageService.get_messages(session, conversation_id)
        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]
