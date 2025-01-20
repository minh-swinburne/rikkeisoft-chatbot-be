from fastapi import APIRouter, HTTPException, status, Depends, Cookie, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import jwt
from app.core.database import get_db
from app.core.config import settings
from app.services import UserService
from app.schemas import GoogleAuthBase, MicrosoftAuthBase, AuthModel, UserBase, SSOBase
import requests


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_microsoft_public_keys():
    discovery_url = (
        f"{settings.microsoft_authority}/v2.0/.well-known/openid-configuration"
    )
    response = requests.get(discovery_url)
    jwks_uri = response.json()["jwks_uri"]
    return requests.get(jwks_uri).json()


MICROSOFT_PUBLIC_KEYS = get_microsoft_public_keys()


@router.post("/native")
async def authenticate_native(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await UserService.get_user_by_username(db, form_data.username)
    if not user:
        user = await UserService.get_user_by_email(db, form_data.username)

    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

    return UserService.grant_access(user)


@router.post("/google")
async def authenticate_google(
    request: GoogleAuthBase,
    db: AsyncSession = Depends(get_db)
):
    user_info = requests.get(
        settings.google_user_info_url,
        headers={"Authorization": f"Bearer {request.access_token}"},
    ).json()

    user = await UserService.get_user_by_provider_sub(db, "google", user_info.get("sub"))

    if not user:
        user_data = UserBase(
            email=user_info.get("email"),
            firstname=user_info.get("given_name"),
            lastname=user_info.get("family_name"),
            avatar_url=user_info.get("picture"),
        )
        user = await UserService.create_user(db, user_data)

        sso_data = SSOBase(
            user_id=user.id,
            provider="google",
            provider_uid=user_info.get("sub"),
        )
        await UserService.create_sso(db, sso_data)

    return UserService.grant_access(user)


@router.post("/microsoft")
async def authenticate_microsoft(
    request: MicrosoftAuthBase,
    db: AsyncSession = Depends(get_db),
    microsoft_public_keys=Depends(get_microsoft_public_keys)
):
    try:
        header = jwt.get_unverified_header(request.id_token)
        key = next(
            key for key in microsoft_public_keys["keys"] if key["kid"] == header["kid"]
        )
        payload = jwt.decode(
            request.id_token,
            key=key,
            algorithms=["RS256"],
            audience=settings.microsoft_client_id,
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    user = await UserService.get_user_by_provider_sub(db, "microsoft", payload["sub"])

    if not user:
        user_data = UserBase(
            email=payload["email"],
            firstname=payload["given_name"],
            lastname=payload["family_name"],
            avatar_url="",
        )
        user = await UserService.create_user(db, user_data)

        sso_data = SSOBase(
            user_id=user.id,
            provider="google",
            provider_uid=payload["sub"],
        )
        await UserService.create_sso(db, sso_data)

    return UserService.grant_access(user)


@router.post("/refresh")
# async def refresh_access_token(refresh_token: str = Cookie(None)):
async def refresh_access_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing"
        )

    refresh_token = authorization.split(" ")[1]  # Extract the token

    # Verify the refresh token
    try:
        access_token = await UserService.refresh_token(refresh_token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    # Create a new access token
    return AuthModel.model_validate({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    })


@router.get("/validate")
# async def validate_token(token: str = Cookie(None)):
async def validate_access(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token missing"
        )

    token = authorization.split(" ")[1]  # Extract the token

    try:
        payload = UserService.validate_token(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return JSONResponse({"valid": True, "payload": payload})
