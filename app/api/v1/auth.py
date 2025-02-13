from fastapi import APIRouter, HTTPException, status, Depends, Body, Cookie, Header
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_pwd_context, validate_access_token
from app.core.database import get_db
from app.core.settings import settings
from app.services import AuthService, UserService
from app.schemas import (
    GoogleAuthBase,
    MicrosoftAuthBase,
    AuthModel,
    TokenModel,
    UserBase,
    SSOModel,
)
from passlib.context import CryptContext


router = APIRouter()


@router.post(
    "/native",
    response_model=AuthModel,
    status_code=status.HTTP_200_OK,
    summary="Authenticate native users using username / email and password",
)
async def authenticate_native(
    form_data: OAuth2PasswordRequestForm = Depends(),
    pwd_context: CryptContext = Depends(get_pwd_context),
    db: AsyncSession = Depends(get_db),
) -> AuthModel:
    user = await UserService.get_user_by_username(db, form_data.username)
    if not user:
        user = await UserService.get_user_by_email(db, form_data.username)

    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # return user  # DEBUG
    return AuthService.grant_access(user, "native")


@router.post(
    "/register",
    response_model=AuthModel,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new native user",
)
async def register_native(
    user_data: UserBase = Body(...),
    pwd_context: CryptContext = Depends(get_pwd_context),
    db: AsyncSession = Depends(get_db),
):
    user = await UserService.get_user_by_username(db, user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username {user_data.username} already exists",
        )

    user = await UserService.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered with another user",
        )

    user_data.password = pwd_context.hash(user_data.password)
    user = await UserService.create_user(db, user_data)
    return AuthService.grant_access(user, "native")


@router.post(
    "/google",
    response_model=AuthModel,
    summary="Authenticate users using Google OAuth2",
)
async def authenticate_google(
    auth_data: GoogleAuthBase = Body(...), db: AsyncSession = Depends(get_db)
):
    user_info = AuthService.get_google_user_info(auth_data.access_token)
    print(user_info)

    new_user = False
    user = await UserService.get_user_by_provider_sub(db, "google", user_info.get("sub"))

    if not user:
        # Create a new user
        user_data = UserBase(
            email=user_info.get("email"),
            firstname=user_info.get("given_name"),
            lastname=user_info.get("family_name"),
            avatar_url=user_info.get("picture"),
        )
        print("\nCreating new Google user..\n")
        user = await UserService.create_user(db, user_data)
        new_user = True

    sso = await UserService.get_sso_by_user_provider(db, user.id, "google")
    if not sso:
        sso_data = SSOModel(
            user_id=user.id,
            provider="google",
            sub=user_info.get("sub"),
            email=user_info.get("email"),
        )
        await UserService.create_sso(db, sso_data)

    return JSONResponse(
        content=AuthService.grant_access(user, "google").model_dump(),
        status_code=status.HTTP_201_CREATED if new_user else status.HTTP_200_OK,
    )


@router.post(
    "/microsoft",
    response_model=AuthModel,
    summary="Authenticate users using Microsoft OAuth2",
)
async def authenticate_microsoft(
    auth_data: MicrosoftAuthBase = Body(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        user_info = AuthService.get_microsoft_user_info(
            auth_data.id_token, auth_data.access_token
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Microsoft ID token",
        )

    new_user = False
    user = await UserService.get_user_by_provider_sub(db, "microsoft", user_info.get("sub"))

    if not user:
        # Create a new user
        from app.aws import s3
        import io
        import os

        image_data = AuthService.get_microsoft_user_photo(auth_data.access_token)
        if image_data is not None:
            file_obj = io.BytesIO(image_data)
            object_name = os.path.join(
                settings.avatar_folder, f"microsoft_{user_info.get("sub")}.jpg"
            )
            s3.upload_file(
                object_name,
                file_obj,
                extra_args={"ContentType": "image/jpeg"},
            )
            avatar_url = (
                f"https://{settings.aws_s3_bucket}.s3.amazonaws.com/{object_name}"
            )

        user_data = UserBase(
            email=user_info.get("email"),
            firstname=user_info.get("given_name"),
            lastname=user_info.get("family_name"),
            avatar_url=avatar_url,
        )
        print("\nCreating new Microsoft user...\n")
        user = await UserService.create_user(db, user_data)
        new_user = True

    try:
        sso = await UserService.get_sso_by_user_provider(db, user.id, "microsoft")
        if not sso:
            sso_data = SSOModel(
                user_id=user.id,
                provider="microsoft",
                sub=user_info.get("sub"),
                email=user_info.get("email"),
            )
            print("\nCreating new Microsoft SSO entry...\n")
            await UserService.create_sso(db, sso_data)
    except Exception as e:
        print(f"Error: {e}")
        await UserService.delete_user(db, user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return JSONResponse(
        content=AuthService.grant_access(user, "microsoft").model_dump(),
        status_code=status.HTTP_201_CREATED if new_user else status.HTTP_200_OK,
    )


@router.get("/validate")
# async def validate_token(token: str = Cookie(None)):
async def validate_access(token_payload: TokenModel = Depends(validate_access_token)):
    """
    Validate the token and return the token payload.
    """
    return JSONResponse({"valid": True, "payload": token_payload.model_dump()})


# not working
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
    return AuthModel.model_validate(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    )
