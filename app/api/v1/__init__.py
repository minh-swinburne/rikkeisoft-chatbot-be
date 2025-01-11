from fastapi import APIRouter
from app.api.v1.docs import router as docs_router
from app.api.v1.chat import router as chat_router
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router



router = APIRouter()
router.include_router(docs_router, prefix="/docs", tags=["Documents"])
router.include_router(chat_router, prefix="/chat", tags=["Chat"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
