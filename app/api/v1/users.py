from fastapi import FastAPI, Depends, HTTPException, status, Form, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from app.core.config import settings
import requests


router = APIRouter()


# Constants for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# FastAPI instance
app = FastAPI()


# Allow CORS from the frontend
origins = [
    "http://localhost:8080",  # Vue frontend URL
    "http://127.0.0.1:8000",  # Local development URL (optional)
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Fake user database
fake_users_db = {
    "tminh1512": {
        "username": "tminh1512",
        "email": "minh@gmail.com",
        "password": "$2a$12$mC5B97wgqzv05s8PBilQDODpRZ.wjwyh1bWSRua7ODBO8H60yjFSu"
    }
}

GOOGLE_CLIENT_ID = settings.google_client_id
GOOGLE_CLIENT_SECRET = settings.google_client_secret
GOOGLE_REDIRECT_URI = settings.google_redirect_uri

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    print(f"Authenticating user: {username}, provided password: {password}")
    print(f"User: {user}")
    if user:
        # Verify the provided password against the hashed password
        if pwd_context.verify(password, user['password']):
            print("Authentication successful")
            return user
    print("Authentication failed")
    return None



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=token&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}"
    }


@router.get("/auth/google")
async def auth_google(code: str):
    print(f"Received code: {code}")
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    print(f"data: {token_url},{data}")
    response = requests.post(token_url, data=data)
    print(f"Token response: {response}")
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
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user


@router.get("/users/me/")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
