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
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Fake user database
fake_users_db = {
    "tminh1512": {
        "id": "c24d9619-848d-4af6-87c8-718444421762",
        "username": "tminh1512",
        "email": "minh@gmail.com",
        "password": "$2a$12$mC5B97wgqzv05s8PBilQDODpRZ.wjwyh1bWSRua7ODBO8H60yjFSu",
        "firstName": "Minh",
        "lastName": "Nguyen",
        "admin": 1,
        "provider": "native",
        "providerUid": 0
    },
    "Ensheath": {
        "id": "117309226250954200649",
        "username": "Ensheath",
        "email": "dvmh2k3@gmail.com",
        "password": "$2a$12$PN2JGhYknKGU2e2oXNA0beW5V760Z7eNWg8q9lLPRzYClBGcfXKNK",
        "firstName": "Hoang",
        "lastName": "Duong",
        "admin": 0,
        "provider": "google",
        "providerUid": 0
    }
}

GOOGLE_CLIENT_ID = settings.google_client_id
GOOGLE_CLIENT_SECRET = settings.google_client_secret
GOOGLE_REDIRECT_URI = settings.google_redirect_uri


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)  # default to 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@router.get("/auth/google")
async def auth_google(code: str):
    print(f"Received code: {code}")    
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {code}"})


    user_data = user_info.json()
    user_id = user_data.get("id")
    user_email = user_data.get("email")
    user_name = user_data.get("name")
    user_picture = user_data.get("picture")

    print(f"User ID: {user_id}")
    print(f"User Email: {user_email}")
    print(f"User Name: {user_name}")
    print(f"User Picture: {user_picture}")


    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id":user_id ,"username": user_name, "email": user_email}, expires_delta=access_token_expires
    )


    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    user_name = user["username"]
    user_email = user.get("email")
    user_id = user.get("id")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"User: {user}")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"id":user_id ,"username": user_name, "email": user_email}, expires_delta=access_token_expires
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
    print("Checking token validity...")
    print(f"Token received: {token}")

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        username: str = payload.get("username")
        email: str = payload.get("email")

        print(f"Decoded payload: {payload}")

        # Ensure 'id', 'username' and 'email' are present
        if id is None or username is None or email is None:
            print(f"Missing required fields. id: {id}, username: {username}, email: {email}")
            raise credentials_exception
    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise credentials_exception

    # Fetch the user from the database using the username
    user = fake_users_db.get(username)

    if user is None:
        print("User not found in the database.")
        raise credentials_exception

    # Now, compare the id and email from the token with the ones in the database
    if user["id"] != id:
        print(f"User ID mismatch. Token ID: {id}, Database ID: {user['id']}")
        raise credentials_exception

    if user["email"] != email:
        print(f"Email mismatch. Token email: {email}, Database email: {user['email']}")
        raise credentials_exception

    print("Token is valid and user authenticated.")
    return user


@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    print("Debug: Token validated and current user retrieved.")
    return current_user

