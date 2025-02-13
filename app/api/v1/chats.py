from fastapi import APIRouter, HTTPException, status, Depends, Path, Body
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import validate_access_token
from app.core.database import get_db
from app.services import ChatService
from app.schemas import (
    ChatBase,
    ChatModel,
    ChatUpdate,
    MessageBase,
    MessageModel,
    TokenModel,
)


router = APIRouter()


@router.get("")
async def get_chat_history(
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> list[ChatModel]:
    try:
        user_id = token_payload.sub
        # Fetch the chats for a given user
        chats = await ChatService.list_chats_by_user_id(db, user_id)
        # print("Chats:", chats)
        return chats
    except Exception as e:
        print("Failed to fetch chat history:", e)
        raise e


@router.post("")
async def create_new_chat(
    chat_data: ChatBase = Body(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> ChatModel:
    if token_payload.sub != chat_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to create this chat",
        )

    chat = await ChatService.create_chat(db, chat_data)
    return chat


@router.get("/{chat_id}")
async def get_conversation(
    chat_id: str = Path(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> list[MessageModel]:
    chat = await ChatService.get_chat_by_id(db, chat_id)
    if not chat or token_payload.sub != chat.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found or you are not authorized to view this chat",
        )

    messages = await ChatService.list_messages_by_chat_id(db, chat_id)
    return messages


@router.post("/{chat_id}", response_model=None)
async def send_query(
    chat_id: str = Path(...),
    message_data: MessageBase = Body(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> MessageModel | StreamingResponse:
    if not message_data.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty"
        )
    if chat_id != message_data.chat_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chat ID in the URL does not match the chat ID in the request body",
        )

    chat = await ChatService.get_chat_by_id(db, chat_id)
    if token_payload.sub != chat.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to send a message to this chat",
        )

    try:
        message = await ChatService.create_message(db, message_data)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message",
        )

    if isinstance(message, MessageModel):
        return message
    else:
        return StreamingResponse(content=message, media_type="text/plain")


@router.get("/{chat_id}/name", response_model=None)
async def generate_chat_name(
    chat_id: str = Path(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> ChatModel | StreamingResponse:
    chat = await ChatService.get_chat_by_id(db, chat_id)
    if token_payload.sub != chat.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to generate a name for this chat",
        )

    chat = await ChatService.generate_name(db, chat_id)

    if isinstance(chat, ChatModel):
        return chat
    else:
        return StreamingResponse(content=chat, media_type="text/plain")


@router.get("/{chat_id}/suggestions")
async def get_suggested_questions(
    chat_id: str = Path(...), db: AsyncSession = Depends(get_db)
):
    # Generate suggestions based on chat history
    suggestions = await ChatService.suggest_message(db, chat_id)
    return JSONResponse({"suggestions": suggestions})


@router.put("/{chat_id}")
async def rename_chat(
    chat_id: str = Path(...),
    updates: ChatUpdate = Body(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
):
    chat = await ChatService.get_chat_by_id(db, chat_id)
    if token_payload.sub != chat.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to rename this chat",
        )

    chat = await ChatService.update_chat_name(db, chat_id, updates.name)

    return chat


@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: str = Path(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
):
    chat = await ChatService.get_chat_by_id(db, chat_id)
    if token_payload.sub != chat.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this chat",
        )

    result = await ChatService.delete_chat(db, chat_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )
    return JSONResponse(
        content={"success": result, "message": "Chat deleted successfully"}
    )
