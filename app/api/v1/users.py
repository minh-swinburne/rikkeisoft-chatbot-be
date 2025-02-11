from fastapi import (
    UploadFile,
    APIRouter,
    HTTPException,
    status,
    Depends,
    Path,
    Body,
    File,
)
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import validate_access_token, get_pwd_context
from app.core.database import get_db
from app.core.settings import settings
from app.services import AuthService, UserService
from app.schemas import (
    AuthModel,
    TokenModel,
    UserModel,
    UserUpdate,
    SSOModel,
    GoogleAuthBase,
    MicrosoftAuthBase,
)
from app.aws import s3
from passlib.context import CryptContext
from typing import Union
import io
import os


router = APIRouter()


@router.get(
    "",
    response_model=list[UserModel],
    response_model_exclude={"password", "username_last_changed"},
)
async def list_users(
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> list[UserModel]:
    if not any(role in ["admin", "system_admin"] for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to view this user",
        )

    users = await UserService.list_users(db)
    return users


@router.get(
    "/me",
    response_model=UserModel,
    response_model_exclude={"password"},
)
async def get_current_user(
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    print("Debug: Token validated and current user retrieved.")
    user_id = token_payload.sub
    user = await UserService.get_user_by_id(db, user_id)
    return user


@router.get("/me/sso", response_model=list[SSOModel])
async def list_sso_current_user(
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> list[SSOModel]:
    sso = await UserService.list_sso_by_user_id(db, token_payload.sub)
    return sso


@router.post("/me/sso/{provider}", response_model=SSOModel)
async def link_sso_current_user(
    provider: str = Path(...),
    auth_data: Union[GoogleAuthBase, MicrosoftAuthBase] = Body(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> SSOModel:
    sso = await UserService.get_sso_by_user_provider(db, token_payload.sub, provider)
    if sso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SSO already linked",
        )

    if provider == "google":
        user_info = AuthService.get_google_user_info(auth_data.access_token)
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Google access token",
            )
    elif provider == "microsoft":
        user_info = AuthService.get_microsoft_user_info(
            auth_data.id_token, auth_data.access_token
        )
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Microsoft access token",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid provider",
        )

    sso = await UserService.get_sso_by_provider_sub(db, provider, user_info.get("sub"))
    if sso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SSO already linked to another user",
        )

    sso_data = SSOModel(
        user_id=token_payload.sub,
        provider=provider,
        sub=user_info.get("sub"),
        email=user_info.get("email"),
    )
    sso = await UserService.create_sso(db, sso_data)
    return sso


@router.delete("/me/sso/{provider}")
async def unlink_sso_current_user(
    provider: str = Path(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    sso = await UserService.get_sso_by_user_provider(db, token_payload.sub, provider)
    if not sso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SSO not found",
        )

    result = await UserService.delete_sso(db, token_payload.sub, provider)
    return JSONResponse({"success": result, "message": "SSO unlinked successfully"})


@router.get(
    "/{user_id}",
    response_model=UserModel,
    response_model_exclude={"password", "username_last_changed"},
)
async def read_user(
    user_id: str = Path(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    if not any(role in ["admin", "system_admin"] for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to view this user",
        )

    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put(
    "/me",
    response_model=AuthModel,
)
async def update_current_user(
    updates: UserUpdate = Body(...),
    token_payload: TokenModel = Depends(validate_access_token),
    pwd_context: CryptContext = Depends(get_pwd_context),
    db: AsyncSession = Depends(get_db),
) -> AuthModel:
    user = await UserService.get_user_by_id(db, token_payload.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if bool(updates.new_password) ^ bool(updates.old_password):
        if not updates.old_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old pasword must be provided",
            )
    if updates.old_password and not pwd_context.verify(
        updates.old_password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password",
        )
    if updates.new_password:
        updates.new_password = pwd_context.hash(updates.new_password)

    user = await UserService.update_user(db, token_payload.sub, updates)
    return AuthService.grant_access(user, token_payload.provider)


@router.put(
    "/{user_id}/role/assign",
    response_model=UserModel,
    response_model_exclude={"password", "username_last_changed"},
)
async def assign_role_to_user(
    user_id: str = Path(...),
    role_name: str = Body(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    if "system_admin" not in token_payload.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to assign roles to users",
        )

    user = await UserService.assign_role(db, user_id, role_name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put(
    "/{user_id}/role/revoke",
    response_model=UserModel,
    response_model_exclude={"password", "username_last_changed"},
)
async def revoke_role_from_user(
    user_id: str = Path(...),
    role_name: str = Body(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    if "system_admin" not in token_payload.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to revoke roles from users",
        )

    user = await UserService.revoke_role(db, user_id, role_name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/me", response_class=JSONResponse)
async def delete_current_user(
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    user_id = token_payload.sub
    result = await UserService.delete_user(db, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return JSONResponse(
        content={"success": result, "message": "User deleted successfully"}
    )


@router.post("/me/avatar")
async def upload_avatar(
    avatar_file: UploadFile = File(...),
    token_payload: TokenModel = Depends(validate_access_token),
):
    from PIL import Image

    file_obj = io.BytesIO(await avatar_file.read())
    avatar_image = Image.open(file_obj).convert("RGB")
    avatar_image.save(file_obj, format="JPEG")
    file_obj.seek(0)

    object_name = os.path.join(settings.avatar_folder, f"{token_payload.sub}.jpg")
    avatar_url = f"https://{settings.aws_s3_bucket}.s3.amazonaws.com/{object_name}"

    s3.upload_file(
        object_name,
        file_obj,
        extra_args={"ContentType": "image/jpeg"},
    )
    return {"url": avatar_url}


@router.delete("/me/avatar")
async def delete_avatar(
    token_payload: TokenModel = Depends(validate_access_token),
) -> JSONResponse:
    object_name = os.path.join(settings.avatar_folder, f"{token_payload.sub}.jpg")
    result = s3.delete_file(object_name)

    return JSONResponse({"success": result, "message": "Avatar deleted successfully"})
