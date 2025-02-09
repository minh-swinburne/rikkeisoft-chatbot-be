# app/core/security.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.core.settings import settings


def setup_cors(app: FastAPI):
    try:
        origins = settings.frontend_origins.split(",")

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,  # List of allowed origins
            allow_credentials=True,
            allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
            allow_headers=["*"],  # Allow all headers
        )
        print("✅ CORS configured. Allowed origins:", origins)
    except Exception as e:
        print("❌ CORS configuration failed:", e)
