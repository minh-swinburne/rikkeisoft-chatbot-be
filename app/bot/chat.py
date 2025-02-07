from sqlalchemy.ext.asyncio import AsyncSession
from groq.types.chat import ChatCompletion, ChatCompletionChunk
from groq import Groq, Stream, RateLimitError
from app.bot.vector_db import search_context
from app.bot import config
from app.core.settings import settings
from app.utils import extract_content
from app.services import UserService, DocumentService
from app.schemas import DocumentModel
from typing import Union
import urllib.parse
import httpx
import re


GROQ_API_KEYS = settings.groq_api_keys.split(",")
current_key_index = 0


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
    user_query = chat_history[-1]["content"]
    context_results = search_context(user_query)
    doc_ids = {result["document_id"] for result in context_results}
    # print("Doc IDs:", doc_ids)

    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")

    user_roles = [role.name for role in user.roles]
    documents: list[DocumentModel] = []
    context = ["| Title | Excerpt | Score |", "| --- | --- | --- |"]
    sources = [
        "| Title | Description | Categories | Created by | Created date | Preview URL | Download URL | Last modified |",
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
            download_url = await DocumentService.generate_document_url(db, doc_id)
            preview_url = (
                document.link_url
                if document.link_url
                else settings.doc_preview_url
                + urllib.parse.quote(download_url, safe="")
            )

            documents.append(document)
            sources.append(
                f"| {document.title} | {re.sub("\n", "<br>", document.description)} | {categories} | {document.creator_user.full_name} | {document.created_date} | {preview_url} | {download_url} | {document.last_modified} |"
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
        context="\n".join(context),
        sources="\n".join(sources),
        user_info=f"- Name: {user.full_name}\n- Email: {user.email}\n- Roles: {', '.join(user_roles)}",
        user_query=user_query,
    )

    for _ in range(len(GROQ_API_KEYS)):
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
