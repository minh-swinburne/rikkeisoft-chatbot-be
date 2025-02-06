from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.services import AuthService
from app.schemas import TokenModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/native")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_pwd_context():
    return pwd_context


async def validate_access_token(
    token: str = Depends(oauth2_scheme),
    # required_roles: list[str] = [],
) -> TokenModel:
    """
    Validate the access token and return its payload if valid.
    """
    try:
        # Decode the token
        payload = AuthService.validate_token(token)
        # Check token type
        if payload.type != "access":
            print("Invalid token type:", payload.type)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # print("Payload:", payload.__dict__)
        return payload  # The token payload can be used for additional checks
    except Exception as e:
        print("Failed to validate token:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
