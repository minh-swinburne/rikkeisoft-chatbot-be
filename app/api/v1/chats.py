from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.chats import ChatBase, ChatResponse
from app.schemas.messages import MessageRequest, MessageResponse
from app.services.chats import *
from app.core.database import get_db
from app.bot.chat import generate_answer, suggest_questions, generate_name


router = APIRouter()


@router.get("/")
async def get_history(user_id: str, db: AsyncSession = Depends(get_db)):
    # Fetch the chats for a given user
    chats = await list_chats(db, user_id)
    return chats


@router.post("/")
async def create_new_chat(request: ChatBase, db: AsyncSession = Depends(get_db)):
    chat = await create_chat(db, request.user_id, request.name)
    return ChatResponse.model_validate({
        "id": chat.id,
        "user_id": chat.user_id,
        "name": chat.name,
        "last_access": chat.last_access
    })


@router.get("/{chat_id}")
async def get_chat(chat_id: str, db: AsyncSession = Depends(get_db)):
    messages = await list_messages(db, chat_id)
    return messages


@router.post("/{chat_id}", response_model=MessageResponse)
async def send_query(chat_id: str, request: MessageRequest, db: AsyncSession = Depends(get_db)):
    if not request:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Create user message
    await create_message(db, {
        "chat_id": chat_id,
        "role": "user",
        "content": request.query
    })

    # Get the chat history (limit to the last 10 messages)
    chat_history = [{"role": message.role, "content": message.content} for message in await list_messages(db, chat_id)][-10:]

# Generate the bot's response (streaming or complete)
    answer = await generate_answer(chat_history)

    if isinstance(answer, str):
        # Complete response: Add message to the database and return
        message = await create_message(db, {
            "chat_id": chat_id,
            "role": "assistant",
            "content": answer
        })

        # Handle new chat name for the first message
        if len(chat_history) == 1:
            new_chat_name = generate_name(chat_history + [{"role": "assistant", "content": answer}])
            await update_chat_name(db, chat_id, new_chat_name.replace("'", ""))

        await update_chat_last_access(db, chat_id)

        return MessageResponse.model_validate({
            "id": message.id,
            "chat_id": message.chat_id,
            "time": message.time,
            "role": message.role,
            "content": message.content
        })
    else:
        # Streaming response: Return a StreamingResponse
        async def stream_generator():
            content = ""
            print("Async generator:", answer)
            async for chunk in answer:  # Handle async generator for streaming
                if chunk:
                    print(chunk, end="")
                    content += chunk
                    yield chunk

            print("\n\nAdding message to database...")
            # Save the full content as a message in the database
            await create_message(db, {
                "chat_id": chat_id,
                "role": "assistant",
                "content": content
            })

            # Handle new chat name for the first message
            if len(chat_history) == 1:
                new_chat_name = generate_name(chat_history + [{"role": "assistant", "content": answer}])
                await update_chat_name(db, chat_id, new_chat_name.replace("'", ""))

            await update_chat_last_access(db, chat_id)

        return StreamingResponse(stream_generator(), media_type="text/plain")


@router.post("/{chat_id}/suggestions")
async def get_suggested_questions(chat_id: str, db: AsyncSession = Depends(get_db)):
    # Get chat history for suggestions (limit to the last 4 messages)
    chat_history = [{"role": message.role, "content": message.content} for message in await list_messages(db, chat_id)][-4:]

    # Generate suggestions based on chat history
    suggestions = suggest_questions(chat_history)
    return {"suggestions": suggestions}


from fastapi import HTTPException

@router.delete("/{chat_id}/delete")
async def delete_chat_endpoint(chat_id: str, db: AsyncSession = Depends(get_db)):
    await delete_chat(db, chat_id)
    return {"message": "Chat deleted successfully"}


@router.put("/{chat_id}/rename")
async def rename_chat(chat_id: str, request: ChatBase, db: AsyncSession = Depends(get_db)):
    chat = await update_chat_name(db, chat_id, request.name)
    return ChatResponse.model_validate({
        "id": chat.id,
        "user_id": chat.user_id,
        "name": chat.name,
        "last_access": chat.last_access
    })
