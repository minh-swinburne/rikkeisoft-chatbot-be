from sentence_transformers import SentenceTransformer
from app.core.config import settings


model = SentenceTransformer(settings.embedding_model)


def get_embedding(text: str | list[str]) -> list[float] | list[list[float]]:
    return model.encode(text).tolist()
