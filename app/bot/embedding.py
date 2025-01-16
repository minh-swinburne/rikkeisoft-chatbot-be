# from sentence_transformers import SentenceTransformer
from app.core.config import settings
from openai import OpenAI


client = OpenAI(api_key=settings.openai_api_key)
# dimension = settings.embedding_dimension
# model = SentenceTransformer(settings.embedding_model)


def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model=settings.embedding_model,
        dimensions=settings.embedding_dimension,
    )

    return response
    # return model.encode(text).tolist()


if __name__ == "__main__":
    print(get_embedding("Your text string goes here"))
    print()
    print(get_embedding(["Your", "text", "string", "goes", "here"]))
