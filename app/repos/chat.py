from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.repos import _commit_and_refresh
from app.schemas import ChatBase, ChatUpdate
from app.models import Chat
from datetime import datetime
from typing import Optional
import uuid6


class ChatRepository:
    @staticmethod
    async def create(db: AsyncSession, chat_data: ChatBase) -> Chat:
        chat = Chat(
            id=str(uuid6.uuid7()),
            **chat_data.model_dump(),
            last_access=datetime.now()
        )
        db.add(chat)
        return await _commit_and_refresh(db, chat)

    @staticmethod
    async def list_by_user_id(db: AsyncSession, user_id: str) -> list[Chat]:
        result = await db.execute(select(Chat).where(Chat.user_id == user_id))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, chat_id: str) -> Optional[Chat]:
        return await db.get(Chat, chat_id)

    @staticmethod
    async def update(db: AsyncSession, chat_id: str, updates: ChatUpdate) -> Chat:
        chat = await ChatRepository.get_by_id(db, chat_id)
        if not chat:
            raise ValueError(f"Chat with ID {chat_id} not found.")

        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(chat, key, value)

        return await _commit_and_refresh(db, chat)

    @staticmethod
    async def update_name(db: AsyncSession, chat_id: str, new_name: str) -> Chat:
        chat = await ChatRepository.get_by_id(db, chat_id)
        if not chat:
            raise ValueError(f"Chat with ID {chat_id} not found.")
        chat.name = new_name
        return await _commit_and_refresh(db, chat)

    @staticmethod
    async def update_last_access(db: AsyncSession, chat_id: str) -> Chat:
        chat = await ChatRepository.get_by_id(db, chat_id)
        chat.last_access = datetime.now()
        return await _commit_and_refresh(db, chat)

    @staticmethod
    async def delete(db: AsyncSession, chat_id: str) -> bool:
        chat = await ChatRepository.get_by_id(db, chat_id)
        if not chat:
            return False
        try:
            await db.delete(chat)
            await db.commit()
        except:
            await db.rollback()
            raise
        return True

    @staticmethod
    async def delete_by_user_id(db: AsyncSession, user_id: str) -> None:
        await db.execute(delete(Chat).where(Chat.user_id == user_id))
        try:
            await db.commit()
        except:
            await db.rollback()
            raise
