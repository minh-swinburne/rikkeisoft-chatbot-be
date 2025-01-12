from fastapi import Depends, Cookie, Header, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from app.schemas.auth import GoogleAuthRequest, MicrosoftAuthRequest
from app.services.users import (
    create_user,
    get_user_by_provider_uid,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    validate_token,
)
from app.core.database import get_db
from app.core.config import settings
from app.utils import parse_timedelta
import requests


router = APIRouter()
# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_microsoft_public_keys():
    discovery_url = f"{settings.microsoft_authority}/v2.0/.well-known/openid-configuration"
    response = requests.get(discovery_url)
    jwks_uri = response.json()["jwks_uri"]
    return requests.get(jwks_uri).json()

MICROSOFT_PUBLIC_KEYS = get_microsoft_public_keys()


def grant_access(
    user_id: str,
    firstname: str,
    lastname: str,
    email: str,
    roles: list,
):
    access_token = create_access_token(
        user_id,
        firstname,
        lastname,
        email,
        roles,
    )

    refresh_token = create_refresh_token(user_id)
    response = JSONResponse({"message": "Login successful"})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production (requires HTTPS)
        samesite="none",
        max_age=parse_timedelta(settings.jwt_access_expires_in).seconds,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False, # Set to True in production (requires HTTPS)
        samesite="none",
        max_age=parse_timedelta(settings.jwt_refresh_expires_in).seconds,
    )
    return response


@router.post("/native")
async def authenticate_native(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return JSONResponse({
        "access_token": create_access_token(
            user.id,
            user.firstname,
            user.lastname,
            user.email,
            ["user"] + (["admin"] if user.admin else []),
            "native"
        ),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer"
    })


@router.post("/google")
async def authenticate_google(request: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):
    user_info = requests.get(
        settings.google_user_info_url,
        headers={"Authorization": f"Bearer {request.access_token}"},
    ).json()

    user = await get_user_by_provider_uid(db, "google", user_info.get("sub"))

    if not user:
        user = await create_user(
            db,
            "", # No username
            user_info.get("email"),
            "", # No password
            user_info.get("given_name"),
            user_info.get("family_name"),
            False,
            "google",
            user_info.get("sub"),
        )

    return JSONResponse({
        "access_token": create_access_token(
            user.id,
            user_info.get("given_name"),
            user_info.get("family_name"),
            user_info.get("email"),
            ["user"],
            "google"
        ),
        "refresh_token": create_refresh_token(user_info.get("sub")),
        "token_type": "bearer"
    })


@router.post("/microsoft")
async def authenticate_microsoft(request: MicrosoftAuthRequest, db: AsyncSession = Depends(get_db)):
    try:
        header = jwt.get_unverified_header(request.id_token)
        key = next(key for key in MICROSOFT_PUBLIC_KEYS["keys"] if key["kid"] == header["kid"])
        payload = jwt.decode(
            request.id_token,
            key=key,
            algorithms=["RS256"],
            audience=settings.microsoft_client_id
            )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )

    # print(f"Received token: {payload}")
    user = await get_user_by_provider_uid(db, "microsoft", payload["sub"])

    if not user:
        user = await create_user(
            db,
            "",
            payload["email"],
            "",
            payload["given_name"],
            payload["family_name"],
            False,
            "microsoft",
            payload["sub"],
        )

    return JSONResponse({
        "access_token": create_access_token(
            user.id,
            payload["given_name"],
            payload["family_name"],
            payload["email"],
            ["user"],
            "microsoft"
        ),
        "refresh_token": create_refresh_token(payload["sub"]),
        "token_type": "bearer"
    })


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
        payload = validate_token(refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )
    if payload["type"] != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
        )

    # Create a new access token
    return JSONResponse({
        "access_token": create_access_token(
            payload["sub"],
            payload["firstname"],
            payload["lastname"],
            payload["email"],
            payload["roles"],
        )
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
        payload = validate_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )

    return JSONResponse({
        "valid": True,
        "payload": payload
    })
