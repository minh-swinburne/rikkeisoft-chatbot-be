from fastapi import APIRouter, HTTPException, Form
from app.bot.chat import generate_answer, suggest_questions
from app.schemas.message import MessageRequest, MessageResponse


router = APIRouter()


# Return current chat (Should add chat_id later for multiple chats)
@router.get("/{chat_id}")
async def get_chat(chat_id: str):
    # Should return messages from the chat
    return {"chat": chat_id}


# Send a message to the chat (Should add chat_id later for multiple chats)
@router.post("/{chat_id}")
async def send_query(chat_id: str, request: MessageRequest) -> MessageResponse:
    if not request:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Should fetch the chat history from the database / cache with the chat_id
    chat_history = []
    answer = generate_answer(request.query, chat_history)
    # Add the bot's response to the chat history in the database
    return MessageResponse.model_validate({"role": "assistant", "content": answer})


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
