from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from app.api.dependencies import validate_access_token
from app.core.config import settings
from app.services import UserService
from app.schemas import TokenModel
import requests


router = APIRouter()


@router.get("/me")
async def read_users_me(token_payload: TokenModel = Depends(validate_access_token)):
    print("Debug: Token validated and current user retrieved.")
    user_id = token_payload.get("sub")
    user = await UserService.get_user_by_id(user_id)
