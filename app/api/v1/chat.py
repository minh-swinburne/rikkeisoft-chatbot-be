from fastapi import APIRouter, HTTPException, Depends
from app.schemas.messages import MessageRequest, MessageResponse
from app.services.chats import create_chat, list_chats, create_message, list_messages
from app.core.database import get_db
from app.bot.chat import generate_answer, suggest_questions
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/")
async def get_history(db: AsyncSession = Depends(get_db)):
    # Fetch the chats for a user (replace with actual user ID)
    user_id = "c24d9619-848d-4af6-87c8-718444421762"
    chats = await list_chats(db, user_id)
    print(chats)
    return chats


@router.post("/")
async def create_chat_endpoint(db: AsyncSession = Depends(get_db)):
    user_id = "c24d9619-848d-4af6-87c8-718444421762"
    chat = await create_chat(db, user_id, "New Chat")
    return {"chat_id": chat.id}


@router.get("/{chat_id}")
async def get_chat(chat_id: str, db: AsyncSession = Depends(get_db)):
    messages = await list_messages(db, chat_id)
    return messages


@router.post("/{chat_id}")
async def send_query(chat_id: str, request: MessageRequest, db: AsyncSession = Depends(get_db)) -> MessageResponse:
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

    # Generate the bot's response
    answer = generate_answer(chat_history)

    # Create bot message
    message = await create_message(db, {
        "chat_id": chat_id,
        "role": "assistant",
        "content": answer
    })

    print("FXXKing message!!!: ", message.__dict__)

    return MessageResponse.model_validate({
        "id": message.id,
        "chat_id": message.chat_id,
        "time": message.time,
        "role": message.role,
        "content": message.content
    })


@router.post("/{chat_id}/suggestions")
async def get_suggested_questions(chat_id: str, db: AsyncSession = Depends(get_db)):
    # Get chat history for suggestions (limit to the last 4 messages)
    chat_history = [{"role": message.role, "content": message.content} for message in await list_messages(db, chat_id)][-4:]

    # Generate suggestions based on chat history
    suggestions = suggest_questions(chat_history)
    return {"suggestions": suggestions}