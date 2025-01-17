from groq import Groq, Stream
from groq.types.chat import ChatCompletion, ChatCompletionChunk
from app.bot import config
from app.bot.vector_db import search_context, query_document
from app.core.config import settings
from app.utils import extract_content
import httpx
import re

client = Groq(
    api_key=settings.groq_api_key,
    timeout=httpx.Timeout(
        timeout=config["timeout"]["total"],
        read=config["timeout"]["read"],
        write=config["timeout"]["write"],
        connect=config["timeout"]["connect"]
        ),
)

async def generate_answer(chat_history: list):
    user_query = chat_history[-1]["content"]
    context_results = search_context(user_query)

#     system_prompt = f"""
# Instructions:
# - Be helpful and answer questions concisely. If you don't know the answer or can't find the relevant documents, let the user know.
# - Utilize the context provided for accurate and specific information.
# - Incorporate your pre-existing knowledge to enhance the depth and relevance of your response.
# - Cite your sources and relevant documents when providing information.

# Context:
# { "\n".join(f"- Title: '{doc["title"]}'\nExcerpt: {doc["text"]}\nScore: {doc["score"]}" for doc in context) }
#     """

    context = "\n".join(f"- Title: '{doc["title"]}'\nExcerpt: {doc["text"]}\nScore: {doc["score"]}" for doc in context_results)
    sources = []

    for title in {doc["title"] for doc in context_results}:
        source = query_document(title)
        if source:
            sources.append(f"- Title: '{title}'\nDescription: {source["description"]}\nCategories: {source["meta"]["categories"]}")

    print(len(context_results))
    print("Context: ", context)
    print("Sources: ", sources)

    system_prompt = config["answer_generation"]["system_prompt"].format(context=context, sources="\n".join(sources))

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            *chat_history,  # Include the last 10 messages in the chat history including the new query
        ],
        **config["answer_generation"]["params"],
    )

    # bot_response = chat_completion.choices[0].message.content

    # return bot_response

    if isinstance(chat_completion, ChatCompletion):
        print("Chat Completion: ", chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content
    else:
        print("Chat Stream: ")
        async def async_stream_generator():
            for chunk in chat_completion:
                yield chunk.choices[0].delta.content
        return async_stream_generator()


def suggest_questions(chat_history: list, context: str = None):
    message_template = config["question_suggestion"]["message_template"]

    #     system_prompt = f"""
    # Instructions:
    # - Suggest 3 to 4 helpful and contextually relevant questions that the user may ask next.
    # - Base your suggestions on the user's chat history and provided context.
    # - Keep the questions concise and relevant to the conversation.
    # - Return suggested questions as a simple ordered list of the questions themselves only, without any additional information, justification or formatting.

    # Format:
    # 1. Question 1?
    # 2. Question 2?
    # 3. Question 3?

    # Chat History: {chat_history}
    # {"Context: " + context if context else ""}
    # Examples: {message_template}
    #     """

    system_prompt = config["question_suggestion"]["system_prompt"].format(
        chat_history=chat_history,
        context=f"\nContext: {context}\n" if context else "",
        message_template="\n".join(f"{i+1}. {question}" for i, question in enumerate(message_template))
    )

    question_completion:ChatCompletion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": ""},
        ],
        # model="llama-3.2-1b-preview",
        # max_tokens=128,
        # temperature=1,
        # top_p=1,
        # stop=None,
        # stream=False,
        **config["question_suggestion"]["params"],
    )

    bot_response = question_completion.choices[0].message.content
    suggested_questions = extract_content(r"^\d+\.\s([^\[\]\*]+?)$", bot_response)

    return suggested_questions if suggested_questions else message_template


def generate_name(chat_history: list):
    #     system_prompt = f"""
    # Instructions:
    # - Generate a name for the chat based on the provided chat history.
    # - The name should be descriptive and relevant to the conversation.
    # - Return ONLY the name as a single sentence or phrase, in plaintext. Nothing else should be included.
    # Chat History: {chat_history}
    # """


    system_prompt = config["name_generation"]["system_prompt"].format(chat_history=chat_history)

    name_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": ""},
        ],
        # model="llama-3.2-1b-preview",
        # max_tokens=8,
        # temperature=1,
        # top_p=1,
        # stop=None,
        # stream=False,
        **config["name_generation"]["params"],
    )

    if isinstance(name_completion, ChatCompletion):
        return re.sub(r"['\"\n]", "", name_completion.choices[0].message.content).strip()
    elif (isinstance(name_completion, Stream[ChatCompletionChunk])):
        for chunk in name_completion:
            yield chunk.choices[0].delta.content

    response = name_completion.choices[0].message.content

    return re.sub(r"['\"\n]", "", response).strip()
