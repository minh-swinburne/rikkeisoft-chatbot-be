from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from app.core.config import settings


app = FastAPI()
model = SentenceTransformer(settings.embedding_model)
dimension = settings.embedding_dimension


@app.post("/embed")
def embed_text(text: str):
    return {"embedding": model.encode(text).tolist()}
