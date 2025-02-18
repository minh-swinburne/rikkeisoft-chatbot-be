from sqlalchemy.ext.asyncio import AsyncSession
from app.repos.message import MessageRepository
from app.repos.chat import ChatRepository
from app.schemas import ChatBase, ChatModel, MessageBase, MessageModel
from typing import AsyncGenerator, Optional
import re


class ChatService:
    """
    Handles business logic for chat management, including CRUD operations for chats and messages.
    """

    @staticmethod
    async def create_chat(db: AsyncSession, chat_data: ChatBase) -> ChatModel:
        """Create a new chat in the database."""
        chat = await ChatRepository.create(db, chat_data)
        return ChatModel.model_validate(chat)

    @staticmethod
    async def create_message(
        db: AsyncSession, message_data: MessageBase, type: str
    ) -> MessageModel | AsyncGenerator[str, None]:
        """Create a new message in the database."""
        from app.bot.chat import generate_answer, summarize_message
        from app.bot.config import load_config

        print("Creating message:", message_data)
        config = load_config()
        length_limit = config["message_summarization"]["length_limit"]
        message = await MessageRepository.create(db, message_data)
        chat_history = [
            {
                "role": message.role,
                "content": message.summary if message.summary else message.content,
            }
            for message in await MessageRepository.list_by_chat_id(
                db, message_data.chat_id, limit=10, descending=True
            )  # 10 most recent messages
        ][::-1]

        chat = await ChatRepository.get_by_id(db, message_data.chat_id)

        try:
            # raise ValueError("Test error")
            # Generate a response based on the chat history
            answer = await generate_answer(chat_history, db, chat.user_id, type)

            if isinstance(answer, str):
                # Complete response: Add message to the database and return
                message = {
                    "chat_id": message_data.chat_id,
                    "role": "assistant",
                    "content": answer,
                }
                if len(answer) > length_limit:
                    summary = summarize_message(answer)
                    message["summary"] = summary
                    print("Summary:", summary)

                message = await MessageRepository.create(
                    db,
                    MessageBase(**message),
                )

                await ChatRepository.update_last_access(db, message_data.chat_id)
                return MessageModel.model_validate(message)
            else:
                # Streaming response: Return a StreamingResponse
                async def stream_generator():
                    content = ""
                    # print("Async generator:", answer)
                    async for chunk in answer:  # Handle async generator for streaming
                        if chunk:
                            # print(chunk, end="")
                            content += chunk
                            yield chunk

                    message = {
                        "chat_id": message_data.chat_id,
                        "role": "assistant",
                        "content": content,
                    }

                    if len(content) > length_limit:
                        # Summarize the full response
                        summary = summarize_message(content)
                        message["summary"] = summary
                        print("Summary:", summary)

                    print("\n\nAdding message to database...")
                    # Save the full content as a message in the database
                    await MessageRepository.create(db, MessageBase(**message))
                    await ChatRepository.update_last_access(db, message_data.chat_id)

                return stream_generator()
        except Exception as e:
            print("Failed to generate answer. Deleting message, ID:", message.id)
            print(e)
            await MessageRepository.delete(db, message.id)
            raise e

    @staticmethod
    async def suggest_message(db: AsyncSession, chat_id: str) -> list[str]:
        """Generate suggested questions based on chat history."""
        from app.bot.chat import suggest_questions

        chat_history = [
            {"role": message.role, "content": message.content}
            for message in await MessageRepository.list_by_chat_id(
                db, chat_id, limit=4, descending=True
            )
        ][::-1]
        return suggest_questions(chat_history)

    @staticmethod
    async def generate_name(
        db: AsyncSession, chat_id: str
    ) -> ChatModel | AsyncGenerator[str, None]:
        """Generate a name for the chat based on chat history."""
        from app.bot.chat import generate_name

        chat_history = [
            {"role": message.role, "content": message.content}
            for message in await MessageRepository.list_by_chat_id(
                db, chat_id, limit=2, descending=True
            )
        ][::-1]

        name = await generate_name(chat_history)

        if isinstance(name, str):
            name = re.sub(r"['\"]", "", name).strip()
            chat = await ChatRepository.update_name(db, chat_id, name)
            return ChatModel.model_validate(chat)
        else:

            async def stream_generator():
                content = ""
                async for chunk in name:
                    if chunk:
                        content += chunk
                        yield chunk
                await ChatRepository.update_name(
                    db, chat_id, re.sub(r"['\"]", "", content)
                )

            return stream_generator()

    @staticmethod
    async def list_chats_by_user_id(db: AsyncSession, user_id: str) -> list[ChatModel]:
        """List all chats for a user."""
        chats = await ChatRepository.list_by_user_id(db, user_id)
        return [ChatModel.model_validate(chat) for chat in chats]

    @staticmethod
    async def list_messages_by_chat_id(
        db: AsyncSession, chat_id: str
    ) -> list[MessageModel]:
        """List all messages in a chat."""
        messages = await MessageRepository.list_by_chat_id(db, chat_id)
        return [MessageModel.model_validate(message) for message in messages]

    @staticmethod
    async def get_chat_by_id(db: AsyncSession, chat_id: str) -> Optional[ChatModel]:
        """Retrieve a chat by ID."""
        chat = await ChatRepository.get_by_id(db, chat_id)
        return ChatModel.model_validate(chat) if chat else None

    @staticmethod
    async def get_message_by_id(
        db: AsyncSession, message_id: str
    ) -> Optional[MessageModel]:
        """Retrieve a message by ID."""
        message = await MessageRepository.get_by_id(db, message_id)
        return MessageModel.model_validate(message) if message else None

    @staticmethod
    async def update_chat_name(db: AsyncSession, chat_id: str, name: str) -> ChatModel:
        """Update the name of a chat."""
        chat = await ChatRepository.update_name(db, chat_id, name)
        return ChatModel.model_validate(chat)

    @staticmethod
    async def delete_chat(db: AsyncSession, chat_id: str) -> bool:
        """Delete a chat from the database."""
        return await ChatRepository.delete(db, chat_id)

    @staticmethod
    async def delete_message(db: AsyncSession, message_id: str) -> bool:
        """Delete a message from the database."""
        return await MessageRepository.delete(db, message_id)
