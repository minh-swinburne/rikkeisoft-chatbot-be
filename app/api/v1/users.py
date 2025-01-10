from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from app.services.users import get_user, authenticate_user
from app.core.database import get_db
from app.core.config import settings
import requests
# from google.oauth2 import id_token
# from google.auth.transport import requests


router = APIRouter()

# Constants for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

GOOGLE_CLIENT_ID = settings.google_client_id
GOOGLE_CLIENT_SECRET = settings.google_client_secret
GOOGLE_REDIRECT_URI = settings.google_redirect_uri


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({
        "iat": datetime.now(),
        "exp": expire
        })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get("/auth/google")
async def auth_google(token: str):
    # try:
    #     # Verify the token with Google's API
    #     idinfo = id_token.verify_oauth2_token(
    #         token, requests.Request(), GOOGLE_CLIENT_ID
    #     )

    #     # Extract user information
    #     user_id = idinfo.get("sub")
    #     email = idinfo.get("email")
    #     name = idinfo.get("name")

    #     return {
    #         "message": "Login successful",
    #         "user_id": user_id,
    #         "email": email,
    #         "name": name,
    #     }

    # except ValueError:
    #     raise HTTPException(status_code=400, detail="Invalid Google token")
    print(f"Received token: {token}")
    token_url = "https://oauth2.googleapis.com/tokeninfo"
    data = {
        "access_token": token,
        # "client_id": GOOGLE_CLIENT_ID,
        # "client_secret": GOOGLE_CLIENT_SECRET,
        # "redirect_uri": GOOGLE_REDIRECT_URI,
        # "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    return response
    print(f"Token response status: {response.status_code}")
    print(f"Token response body: {response.json()}")

    if response.status_code != 200:
        return {"error": response.json()}

    access_token = response.json().get("access_token")
    print(f"Access token: {access_token}")

    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    print(f"User info response status: {user_info.status_code}")
    print(f"User info response body: {user_info.json()}")

    return user_info.json()


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"User: {user}")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "sub": user.id,
            "username": user.username,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "admin": user.admin,
        },
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user(db, user_id)
    if user is None:
        raise credentials_exception
    return user


@router.get("/users/me/")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
