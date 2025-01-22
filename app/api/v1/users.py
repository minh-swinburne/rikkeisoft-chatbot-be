from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import validate_access_token
from app.core.database import get_db
from app.services import UserService
from app.schemas import TokenModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import requests


router = APIRouter()


@router.get("/me")
async def read_users_me(token_payload: TokenModel = Depends(validate_access_token), db: AsyncSession = Depends(get_db)):
    print("Debug: Token validated and current user retrieved.")
    user_id = token_payload.sub
    user = await UserService.get_user_by_id(db, user_id)
    return user
