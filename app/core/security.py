# app/core/security.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def setup_cors(app: FastAPI):
    try:
        origins = [
            "http://localhost:8080",  # Vue frontend URL
            "http://localhost:5173",  # Vue frontend URL 2
            "http://127.0.0.1:8000",  # Local development URL (optional)
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,  # List of allowed origins
            allow_credentials=True,
            allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
            allow_headers=["*"],  # Allow all headers
        )
        print("✅ CORS configured")
    except Exception as e:
        print("❌ CORS configuration failed:", e)
