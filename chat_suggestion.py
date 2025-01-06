from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Initialize FastAPI
app = FastAPI()

# Allow CORS from the frontend
origins = [
    "http://localhost:8080",  # Vue frontend URL
    "http://127.0.0.1:8000",  # Local development URL (optional)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
    
class ChatMessage(BaseModel):
    message: str

@app.post("/suggestions")
async def get_suggestions(chat_message: ChatMessage):
    message = chat_message.message
    print(message)
    return {"suggestions": [message]}
