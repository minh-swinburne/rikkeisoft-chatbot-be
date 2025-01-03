from fastapi import APIRouter, HTTPException
import httpx


router = APIRouter()


# Return current chat (Should add chat_id later for multiple chats)
@router.get("/")
async def get_chat():
    # Should return messages from the chat
    return {"chat": "chat_id"}


# Send a message to the chat (Should add chat_id later for multiple chats)
@router.post("/")
async def send_message(message: str):
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Should send the bot's answer to the chat
    return {"answer": "answer"}