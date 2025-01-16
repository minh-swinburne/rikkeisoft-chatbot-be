from sentence_transformers import SentenceTransformer
from app.core.config import settings


model = SentenceTransformer(settings.embedding_model)
dimension = settings.embedding_dimension


def embed_text(text: str) -> list[float]:
    return model.encode(text).tolist()