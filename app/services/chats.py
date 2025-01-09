from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Chat, Message
from app.schemas import MessageResponse
from datetime import datetime

import uuid

# CRUD operation to create a new chat
async def create_chat(db: AsyncSession, user_id: str, name: str):
    chat = Chat(id=str(uuid.uuid4()), user_id=user_id, name=name,last_access=datetime.now())
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


# CRUD operation to list chats for a user
async def list_chats(db: AsyncSession, user_id: str):
    result = await db.execute(select(Chat).where(Chat.user_id == user_id))
    return result.scalars().all()


# CRUD operation to create a new message
async def create_message(db: AsyncSession, message: dict):
    message_id = str(uuid.uuid4())
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
async def list_messages(db: AsyncSession, chat_id: str):
    result = await db.execute(select(Message).where(Message.chat_id == chat_id))
    return result.scalars().all()