from sentence_transformers import SentenceTransformer
from app.core.config import settings

model = SentenceTransformer(settings.embedding_model)

def get_embedding(text: str | list[str]) -> list[float] | list[list[float]]:
    # return [0.0] * settings.embedding_dimension # turn off embedding for now
    return model.encode(text).tolist()
