from fastapi import APIRouter, HTTPException, status, Depends, Path, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import validate_access_token
from app.core.database import get_db
from app.services import UserService
from app.schemas import TokenModel, UserModel, UserUpdate


router = APIRouter()


@router.get("/me", response_model=UserModel)
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
    response_model=UserModel,
    response_model_exclude={"password", "username_last_changed"},
)
async def update_user_me(
    user_update: UserUpdate = Body(...),
    token_payload: TokenModel = Depends(validate_access_token),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    user = await UserService.update_user(db, token_payload.sub, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


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
    if not any(role in ["admin", "system_admin"] for role in token_payload.roles):
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
    if not any(role in ["admin", "system_admin"] for role in token_payload.roles):
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
) -> bool:
    user_id = token_payload.sub
    result = await UserService.delete_user(db, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return JSONResponse(
        content={"success": result, "message": "User deleted successfully"}
    )
