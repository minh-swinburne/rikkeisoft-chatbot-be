from fastapi import APIRouter
from . import docs, chats, users, auth, config


router = APIRouter()

router.include_router(docs.router, prefix="/docs", tags=["Documents"])
router.include_router(chats.router, prefix="/chats", tags=["Chats"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(config.router, prefix="/config", tags=["Configuration"])
