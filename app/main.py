from fastapi import FastAPI
from app.core.security import setup_cors
from app.core.database import setup_database
from app.bot.vector_db import setup_vector_db
from app.api import router


app = FastAPI()
app.include_router(router, prefix="/api")

setup_cors(app)
setup_database()
setup_vector_db()


@app.get("/")
def read_root():
    return {"Hello": "World"}
