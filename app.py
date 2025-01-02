from fastapi import FastAPI, HTTPException
import httpx
import json

# Initialize FastAPI
app = FastAPI()

# GroqCloud API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Update to correct Groq API endpoint
GROQ_API_KEY = "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"  # Groq API Key

# Function to interact with GroqCloud API
async def get_groq_answer(query: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Constructing the Groq API payload
    payload = {
        "model": "llama-3.3-70b-versatile",  # Replace with your model name
        "messages": [{"role": "user", "content": query}]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return GroqCloud API response
    else:
        raise HTTPException(status_code=response.status_code, detail="Error interacting with GroqCloud")

# Define a FastAPI endpoint to handle queries
@app.get("/generate-answer")
async def generate_answer(query: str):
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")

    answer = await get_groq_answer(query)
    return {"answer": answer}
