from fastapi import File, UploadFile, APIRouter, HTTPException, status, Depends, Path, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import validate_access_token, get_pwd_context
from app.core.database import get_db
from app.core.settings import settings
from app.services import AuthService, UserService
from app.schemas import AuthModel, TokenModel, UserModel, UserUpdate
from passlib.context import CryptContext
from app.aws import s3
import io
import os


router = APIRouter()


@router.get(
    "/me",
    response_model=UserModel,
    response_model_exclude={"password", "username_last_changed"}
)
async def read_users_me(
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    print("Debug: Token validated and current user retrieved.")
    user_id = token_payload.sub
    user = await UserService.get_user_by_id(db, user_id)
    return user


@router.get(
    "",
    response_model=list[UserModel],
    response_model_exclude={"password", "username_last_changed"},
)
async def read_users(
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> list[UserModel]:
    if not any(role in ["admin", "system_admin"] for role in token_payload.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to view this user",
        )

    users = await UserService.get_users(db)
    return users


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
async def update_user_me(
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old pasword must be provided.")
    if updates.new_password:
        if not pwd_context.verify(updates.old_password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password.")
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
async def delete_user_me(
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


@router.post("/avatar/upload")
async def upload_avatar(
    avatar_file: UploadFile = File(...),
    token_payload: TokenModel = Depends(validate_access_token),
):
    user_id = token_payload.sub
    if avatar_file is not None:
        file_obj = io.BytesIO(await avatar_file.read())
        object_name = os.path.join(
            settings.avatar_folder, f"{user_id}.jpg"
        )
        s3.upload_file(
            object_name,
            file_obj,
            extra_args={"ContentType": "image/jpeg"},
        )
        avatar_url = (
            f"https://{settings.aws_s3_bucket}.s3.amazonaws.com/{object_name}"
        )
        return {"url": avatar_url}