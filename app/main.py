from fastapi import FastAPI
from app.core.security import setup_cors
from app.api.v1 import router as api_router


app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

setup_cors(app)

@app.get("/")
def read_root():
    return {"Hello": "World"}