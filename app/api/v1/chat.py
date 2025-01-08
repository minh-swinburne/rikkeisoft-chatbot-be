from fastapi import APIRouter, HTTPException, Form
from app.bot.chat import generate_answer, suggest_questions
from app.repos.chat import ChatRepository
from app.schemas.message import MessageRequest, MessageResponse
from datetime import datetime


router = APIRouter()
repository = ChatRepository()


@router.get("/")
async def get_history():
    return repository.list_chats()


@router.post("/")
async def create_chat():
    chat = repository.create_chat({
        "user_id": "c24d9619-848d-4af6-87c8-718444421762",
        "name": "New Chat",
    })
    return {"chat_id": chat["id"]}


# Return current chat (Should add chat_id later for multiple chats)
@router.get("/{chat_id}")
async def get_chat(chat_id: str):
    # Should return messages from the chat
    return repository.list_messages(chat_id)


# Send a message to the chat (Should add chat_id later for multiple chats)
@router.post("/{chat_id}")
async def send_query(chat_id: str, request: MessageRequest) -> MessageResponse:
    if not request:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # print(f"Received chat_id: {chat_id}")
    # print(f"Received request body: {request}")

    repository.create_message({
        "chat_id": chat_id,
        "time": datetime.now(),
        "role": "user",
        "content": request.query
    })

    # Should fetch the chat history from the database / cache with the chat_id
    chat_history = [{
        "role": message["role"],
        "content": message["content"],
    } for message in repository.list_messages(chat_id)][-10:]

    answer = generate_answer(chat_history)

    # Add the bot's response to the chat history in the database / cache
    message = repository.create_message({
        "chat_id": chat_id,
        "time": datetime.now(),
        "role": "assistant",
        "content": answer,
    })

    return MessageResponse.model_validate(message)


@router.post("/{chat_id}/suggestions")
async def get_suggested_questions(chat_id: str):
    # Should fetch the chat history from the database / cache with the chat_id
    chat_history = [
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message in repository.list_messages(chat_id)
    ][-4:]

    return {"suggestions": suggest_questions(chat_history)}
