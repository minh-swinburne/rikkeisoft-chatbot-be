from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Chat, Message
from app.schemas import MessageResponse
from datetime import datetime

import uuid6

# CRUD operation to create a new chat
async def create_chat(db: AsyncSession, user_id: str, name: str) -> Chat:
    chat = Chat(
        id=str(uuid6.uuid7()),
        user_id=user_id,
        name=name,
        last_access=datetime.now()
    )
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


# CRUD operation to list chats for a user
async def list_chats(db: AsyncSession, user_id: str) -> list[Chat]:
    result = await db.execute(select(Chat).where(Chat.user_id == user_id))
    return result.scalars().all()


async def get_chat_by_id(db: AsyncSession, chat_id: str) -> Chat:
    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    return result.scalar_one_or_none()


async def update_chat_name(db: AsyncSession, chat_id: str, name: str) -> Chat:
    chat = await get_chat_by_id(db, chat_id)
    chat.name = name

    await db.commit()
    await db.refresh(chat)
    return chat


async def update_chat_last_access(db: AsyncSession, chat_id: str) -> Chat:
    chat = await get_chat_by_id(db, chat_id)
    chat.last_access = datetime.now()

    await db.commit()
    await db.refresh(chat)
    return chat


# CRUD operation to create a new message
async def create_message(db: AsyncSession, message: dict) -> Message:
    message_id = str(uuid6.uuid7())
    item = Message(
        id=message_id,
        chat_id=message["chat_id"],
        time=datetime.now(),
        role=message["role"],
        content=message["content"]
    )

    db.add(item)
    await db.commit()
    await db.refresh(item)

    return item


# CRUD operation to list messages in a chat
async def list_messages(db: AsyncSession, chat_id: str) -> list[Message]:
    result = await db.execute(select(Message).where(Message.chat_id == chat_id))
    return result.scalars().all()