from groq import Groq
from app.bot.vector_db import search_context
from app.core.config import settings
from app.utils import extract_content
import httpx
import re

client = Groq(
    api_key=settings.groq_api_key,
    timeout=httpx.Timeout(20.0, read=5.0, write=10.0, connect=2.0),
)

def generate_answer(chat_history: list):
    user_query = chat_history[-1]["content"]
    context = search_context(user_query)

    system_prompt = f"""
Instructions:
- Be helpful and answer questions concisely. If you don't know the answer or can't find the relevant documents, let the user know.
- Utilize the context provided for accurate and specific information.
- Incorporate your pre-existing knowledge to enhance the depth and relevance of your response.
- Cite your sources and relevant documents when providing information.

Context:
{ "\n".join(f"- Title: '{doc["title"]}'\nExcerpt: {doc["text"]}\nScore: {doc["score"]}" for doc in context) }
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            *chat_history,  # Include the last 10 messages in the chat history including the new query (to be fetched from the database)
        ],
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        temperature=0.5,
        top_p=1.0,
        stop=None,
        stream=False,
    )

    bot_response = chat_completion.choices[0].message.content

    # print()
    # print("Chat History:")
    # print("\n".join("{}: {}".format(*k) for k in enumerate(chat_history)))
    # print()
    # print(chat_completion.choices[0])

    return bot_response


def suggest_questions(chat_history: list, context: str = None):
    message_template = [
        "What is the summary of the document?",
        "Who created this document?",
        "What are the main points?",
        "When was this document uploaded?",
        "Can you provide a detailed explanation?",
    ]

    # print("\n".join("{}: {}".format(*k) for k in enumerate(chat_history)))

    system_prompt = f"""
Instructions:
- Suggest 3 to 4 helpful and contextually relevant questions that the user may ask next.
- Base your suggestions on the user's chat history and provided context.
- Keep the questions concise and relevant to the conversation.
- Return suggested questions as a simple ordered list of the questions themselves only, without any additional information, justification or formatting.
Format: "1. [Question 1]?\n2. [Question 2]?\n3. [Question 3]?"
Chat History: {chat_history}
{"Context: " + context if context else ""}
Examples: {message_template}
    """

    question_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": ""},
        ],
        model="llama-3.2-1b-preview",
        max_tokens=128,
        temperature=1,
        top_p=1,
        stop=None,
        stream=False,
    )

    bot_response = question_completion.choices[0].message.content
    suggested_questions = extract_content(r"^\d+\.\s([^\[\]\*]+?)$", bot_response)

    return suggested_questions if suggested_questions else message_template


def generate_name(chat_history: list):
    system_prompt = f"""
Instructions:
- Generate a name for the chat based on the provided chat history.
- The name should be descriptive and relevant to the conversation.
- Return ONLY the name as a single sentence or phrase, in plaintext. Nothing else should be included.
Chat History: {chat_history}
"""

    name_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": ""},
        ],
        model="llama-3.2-1b-preview",
        max_tokens=8,
        temperature=1,
        top_p=1,
        stop=None,
        stream=False,
    )

    response = name_completion.choices[0].message.content

    return re.sub(r"['\"\n]", "", response).strip()
