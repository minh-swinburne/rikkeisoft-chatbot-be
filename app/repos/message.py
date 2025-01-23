from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, desc
from app.repos import _commit_and_refresh
from app.schemas import MessageBase
from app.models import Message
from datetime import datetime
from typing import Optional
import uuid6


class MessageRepository:
    @staticmethod
    async def create(db: AsyncSession, message_data: MessageBase) -> Message:
        """
        Create a new message record.
        """
        message = Message(
            id=str(uuid6.uuid7()),
            **message_data.model_dump(),
            time=datetime.now(),
        )
        db.add(message)
        return await _commit_and_refresh(db, message)

    @staticmethod
    async def list_by_chat_id(
        db: AsyncSession, chat_id: str, limit: int = None, descending: bool = False
    ) -> list[Message]:
        """
        List all messages for a specific chat.
        """
        result = await db.execute(
            select(Message).where(Message.chat_id == chat_id)
            .order_by(desc(Message.time) if descending else Message.time)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, message_id: str) -> Optional[Message]:
        """
        Get a message by its ID.
        """
        return await db.get(Message, message_id)

    @staticmethod
    async def update_content(
        db: AsyncSession, message_id: str, new_content: str
    ) -> Message:
        """
        Update the content of a specific message.
        """
        message = await MessageRepository.get_by_id(db, message_id)
        if not message:
            raise ValueError(f"Message with ID {message_id} not found.")
        message.content = new_content
        return await _commit_and_refresh(db, message)

    @staticmethod
    async def delete(db: AsyncSession, message_id: str) -> bool:
        """
        Delete a specific message by its ID.
        """
        message = await MessageRepository.get_by_id(db, message_id)
        if not message:
            return False
        try:
            await db.delete(message)
            await db.commit()
        except:
            await db.rollback()
            raise
        return True

    @staticmethod
    async def delete_by_chat_id(db: AsyncSession, chat_id: str) -> bool:
        """
        Delete all messages associated with a specific chat.
        This is optional because cascading in the DB already handles this.
        """
        await db.execute(delete(Message).where(Message.chat_id == chat_id))
        try:
            await db.commit()
        except:
            await db.rollback()
            raise
        return True
