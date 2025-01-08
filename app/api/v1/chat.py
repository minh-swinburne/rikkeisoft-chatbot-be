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

    repository.create({
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
    message = repository.create({
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
            "role": "user",
            "content": "What gifts should I give my father on his birthday?",
        },
        {
            "role": "assistant",
            "content": "The ideal gift for your father's birthday depends on his interests, hobbies, and preferences. Here are some popular gift ideas:\n\n1. **Personalized items**: Engraved watch, monogrammed wallet, or a photo album with fond memories.\n2. **Tech gadgets**: Smartwatch, wireless headphones, or a high-tech smartphone accessory.\n3. **Experiences**: Tickets to a sporting event or a concert, a weekend getaway, or a fun activity he's always wanted to try (e.g., golfing, fishing, or cooking class).\n4. **Luxury grooming**: High-quality shaving kit, luxurious fragrances, or a rejuvenating spa day.\n5. **Hobby-related gifts**: If your father enjoys a particular hobby, consider gifting him something related, such as:\n\t* For the outdoorsy type: camping gear, hiking equipment, or a new bike.\n\t* For the foodie: cookbook, wine and cheese basket, or a kitchen appliance.\n\t* For the sports enthusiast: autographed jersey, sports memorabilia, or a new piece of equipment.\n6. **Practical items**: A high-quality wallet, a leather bag, or a functional tool for his workshop or garage.\n7. **Subscription services**: Sign him up for a streaming platform, a monthly wine club, or a magazine subscription that aligns with his interests.\n\nRemember, the most important aspect of a gift is the thought and love behind it. Choose something that shows you care and pay attention to his interests and preferences.\n\nSources:\n- Various online gift guides and reviews (e.g., The Spruce, Wirecutter, and Esquire).\n- Personal experience and common gift-giving practices.",
        },
    ]

    return {"suggestions": suggest_questions(chat_history)}
