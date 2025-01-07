from fastapi import APIRouter, HTTPException, Form
from app.bot.chat import generate_answer
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter()


# Return current chat (Should add chat_id later for multiple chats)
@router.get("/{chat_id}")
async def get_chat(chat_id: str):
    # Should return messages from the chat
    return {"chat": chat_id}


# Send a message to the chat (Should add chat_id later for multiple chats)
@router.post("/{chat_id}")
async def send_query(chat_id: str, request: ChatRequest) -> ChatResponse:
    if not request:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Should fetch the chat history from the database with the chat_id
    answer = generate_answer(request.query, [])
    # Add the bot's response to the chat history in the database
    return ChatResponse.model_validate({"role": "assistant", "content": answer})


@router.post("/{chat_id}/suggestions")
async def upload_file(chat_id: str, file: bytes = Form(...)):
    # Should save the file to the database and return the file_id
    return {"file_id": "12345"}