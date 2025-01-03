from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx


def get_api_key():
    with open("api_key.txt") as f:
        return f.read().strip()


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

# GroqCloud API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = get_api_key()  # Groq API Key


# Function to interact with GroqCloud API
async def get_answer(query: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    # Constructing the Groq API payload
    payload = {
        "model": "llama-3.3-70b-versatile",  # Replace with your model name
        "messages": [{"role": "user", "content": query}],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return GroqCloud API response
    else:
        raise HTTPException(
            status_code=response.status_code, detail="Error interacting with GroqCloud"
        )


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Define a FastAPI endpoint to handle queries
@app.get("/generate-answer")
async def generate_answer(query: str):
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")

    answer = await get_answer(query)
    return {"answer": answer}
