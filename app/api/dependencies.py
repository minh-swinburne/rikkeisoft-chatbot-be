from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services import UserService
from app.schemas import TokenModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/native")


async def validate_access_token(
    token: str = Depends(oauth2_scheme),
    # required_roles: list[str] = [],
) -> TokenModel:
    """
    Validate the access token and return its payload if valid.
    """
    try:
        # Decode the token
        payload = UserService.validate_token(token)
        # Check token type
        if payload.type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # user_roles = payload.get("roles", [])
        # if not any(role in required_roles for role in user_roles):
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Insufficient permissions",
        #         headers={"WWW-Authenticate": "Bearer"},
        #     )

        print(payload.__dict__)
        return payload  # The token payload can be used for additional checks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
