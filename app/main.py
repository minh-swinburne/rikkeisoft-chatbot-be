from fastapi import FastAPI
from app.core.security import setup_cors
from app.core.database import setup_database
from app.bot.vector_db import setup_vector_db
from app.bot.chat import setup_chatbot
from app.api import router


app = FastAPI()
app.include_router(router, prefix="/api")

setup_cors(app)
setup_database()
setup_vector_db()
setup_chatbot()


@app.get("/")
def read_root():
    return {
        "app": "RikkeiGPT API",
        "version": "1.0.0",
        "status": "running",
        "language": "Python 3.12.8",
        "framework": "FastAPI 0.115.7",
        "database": "MySQL 8.0.40",
        "server": "ECS Fargate",
        "message": "Welcome to the RikkeiGPT API. Visit /docs for the API documentation.",
    }
