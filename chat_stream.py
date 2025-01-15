from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv(override=True)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def chat_stream():
    stream = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "you are a helpful assistant."},
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            },
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=True,
    )

    # Print the incremental deltas returned by the LLM.
    for chunk in stream:
        yield chunk.choices[0].delta.content or ""

for chunk in chat_stream():
    print(chunk, end="")
