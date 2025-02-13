from sqlalchemy.ext.asyncio import AsyncSession
from groq.types.chat import ChatCompletion, ChatCompletionChunk
from groq import Groq, Stream, RateLimitError, APIStatusError
from app.bot.vector_db import search_context
from app.bot.config import load_config
from app.core.settings import settings
from app.utils import extract_content
from app.services import UserService, DocumentService
from app.schemas import DocumentModel
from typing import Union
import httpx
import re


GROQ_API_KEYS = settings.groq_api_keys.split(",")

current_key_index = 0
client = None


def setup_chatbot():
    global client

    config = load_config()
    client = Groq(
        api_key=GROQ_API_KEYS[0],
        timeout=httpx.Timeout(
            timeout=config["timeout"]["total"],
            read=config["timeout"]["read"],
            write=config["timeout"]["write"],
            connect=config["timeout"]["connect"],
        ),
    )


async def generate_answer(chat_history: list[dict], db: AsyncSession, user_id: str):
    global current_key_index

    config = load_config()
    last_qa = [message["content"] for message in chat_history[-3:]]
    context_results = search_context(last_qa)

    doc_ids = {result["document_id"] for result in context_results}
    # print("Last QA:", last_qa)
    print("Doc IDs:", doc_ids)

    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")

    user_roles = [role.name for role in user.roles]
    documents: list[DocumentModel] = []
    context = ["| Title | Excerpt | Score |", "| --- | --- | --- |"]
    sources = [
        "| Title | Description | Categories | Created by | Created date | Preview URL | Last modified |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for doc_id in doc_ids:
        document = await DocumentService.get_document_by_id(db, doc_id)
        if not document:
            continue

        restricted = document.restricted
        if not restricted or any(
            role in ["admin", "system_admin"] for role in user_roles
        ):
            categories = [cat.name for cat in document.categories]
            preview_url = await DocumentService.generate_document_url(db, doc_id, preview=True)

            documents.append(document)
            sources.append(
                f"| {document.title} | {re.sub("\n", "<br>", document.description)} | {categories} | {document.creator_user.full_name} | {document.created_date} | {preview_url} | {document.last_modified} |"
            )

    for result in context_results:
        document_id = result["document_id"]
        document = next((doc for doc in documents if doc.id == document_id), None)
        if not document:
            continue

        context.append(
            f"| {document.title} | {re.sub("\n", "<br>", result["text"])} | {result["score"]} |"
        )

    # print(len(context_results))
    # print("\nContext:\n", context)
    # print("\nSources:\n", sources)

    system_prompt = config["answer_generation"]["system_prompt"].format(
        user_info=f"- Name: {user.full_name}\n- Email: {user.email}\n- Roles: {', '.join(user_roles)}",
    )
    chat_history[-1]["content"] = (
        chat_history[-1]["content"]
        + "Here is some relevant information:\n"
        + "  - Context:\n"
        + "\n".join(context)
        + "\n  - Sources:\n"
        + "\n".join(sources)
    )

    for _ in range(len(GROQ_API_KEYS) + 1):
        try:
            chat_completion: Union[ChatCompletion, Stream[ChatCompletionChunk]] = (
                client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *chat_history,  # Include the last 10 messages in the chat history including the new query
                    ],
                    **config["answer_generation"]["params"],
                )
            )
            break
        except RateLimitError as e:
            print("❌ Rate Limit Error:", e)
            current_key_index += 1
            current_key_index %= len(GROQ_API_KEYS)
            client.api_key = GROQ_API_KEYS[current_key_index]
        except APIStatusError as e:  # Request is too large
            print("❌ API Status Error:", e)
            print("System prompt length:", len(system_prompt))
            print(
                "Chat history length (excluding last message):",
                sum(len(message["content"]) for message in chat_history[:-1]),
            )
            print(
                "Last message length (including context & sources):",
                len(chat_history[-1]["content"]),
            )
            length_limit = config["message_summarization"]["length_limit"]
            for message in chat_history[:-1]:
                old_length = len(message["content"])
                if len(message["content"]) > length_limit:
                    message["content"] = summarize_message(message["content"])
                    print("Summarized message length:", old_length, "->", len(message["content"]))
            print("Retrying...")
            continue
        except Exception as e:
            print("❌ Error:", e)
            break

    if isinstance(chat_completion, ChatCompletion):
        print("Chat Completion: ", chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content
    else:
        print("Chat Stream: ")

        async def async_stream_generator():
            for chunk in chat_completion:
                yield chunk.choices[0].delta.content

        return async_stream_generator()


def summarize_message(answer: str):
    config = load_config()
    system_prompt = config["message_summarization"]["system_prompt"]
    answer_completion: ChatCompletion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": answer},
        ],
        **config["message_summarization"]["params"],
    )
    bot_response = answer_completion.choices[0].message.content
    return bot_response


def suggest_questions(chat_history: list, context: str = None):
    config = load_config()
    message_template = config["question_suggestion"]["message_template"]

    system_prompt = config["question_suggestion"]["system_prompt"].format(
        chat_history=chat_history,
        context=f"\nContext: {context}\n" if context else "",
        message_template="\n".join(
            f"{i+1}. {question}" for i, question in enumerate(message_template)
        ),
    )

    question_completion: ChatCompletion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": ""},
        ],
        **config["question_suggestion"]["params"],
    )

    bot_response = question_completion.choices[0].message.content
    suggested_questions = extract_content(r"^\d+\.\s([^\[\]\*]+?)$", bot_response)

    return suggested_questions if suggested_questions else message_template


async def generate_name(chat_history: list):
    config = load_config()
    system_prompt = config["name_generation"]["system_prompt"].format(
        chat_history=chat_history
    )

    name_completion: Union[ChatCompletion, Stream[ChatCompletionChunk]] = (
        client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": ""},
            ],
            **config["name_generation"]["params"],
        )
    )

    if isinstance(name_completion, ChatCompletion):
        return re.sub(
            r"['\"\n]", "", name_completion.choices[0].message.content
        ).strip()
    else:

        async def async_stream_generator():
            for chunk in name_completion:
                yield chunk.choices[0].delta.content

        return async_stream_generator()
