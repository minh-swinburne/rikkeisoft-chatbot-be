from groq import Groq
from app.core.config import settings
from app.utils import extract_content
import httpx

client = Groq(
    api_key=settings.groq_api_key,
    timeout=httpx.Timeout(20.0, read=5.0, write=10.0, connect=2.0),
)

def generate_answer(chat_history: list):
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
    return bot_response

def suggest_questions(chat_history: list, context: str = None):
    message_template = [
        "What is the summary of the document?",
        "Who created this document?",
        "What are the main points?",
        "When was this document uploaded?",
        "Can you provide a detailed explanation?",
    ]

    print(chat_history)

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
    suggested_questions = extract_content(r"^\d+\.\s(.+)$", bot_response)

    return suggested_questions if suggested_questions else message_template
