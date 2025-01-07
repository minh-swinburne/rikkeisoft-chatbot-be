from groq import Groq
from app.core.config import settings

def generate_answer(query: str, chat_history: list):
    client = Groq(api_key=settings.groq_api_key)
    system_prompt = f"""
Instructions:
- Be helpful and answer questions concisely. If you don't know the answer or can't find the relevant documents, let the user know.
- Utilize the context provided for accurate and specific information.
- Incorporate your preexisting knowledge to enhance the depth and relevance of your response.
- Cite your sources and relevant documents when providing information.
Context: Answer the following question.
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            *chat_history[-10:],  # Include the last 10 messages in the chat history (to be fetched from the database)
            {"role": "user", "content": query},
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_tokens=1024,
        top_p=1.0,
        stop=None,
        stream=False,
    )

    bot_response = chat_completion.choices[0].message.content
    return bot_response
