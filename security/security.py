"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: This module contains security setup for my app, NOT YET IMPLEMENTED, secret key does nothing
"""
from typing import Union, Annotated

from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from database.database import collection_auth

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from fastapi import Form


class OAuth2PasswordRequestFormEmail:
    def __init__(
        self,
        user_email: str = Form(...),
        password: str = Form(...),
        scope: str = Form(default=""),
        client_id: str = Form(None),
        client_secret: str = Form(None),
    ):
        self.user_email = user_email
        self.password = password
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_email: str | None = None

class AuthUser(BaseModel):
    email: str | None = None
    disabled: bool | None = None

class UserInDB(AuthUser):
    hashed_password: str

def get_password_hash(password):
    """
    this function utilizes CryptContext bcrypt to hash parameter "password"
    """
    return pwd_context.hash(password)

def get_user(user_email: str):
    """
    utilizes pymongo library to get user from users collection
    """
    user_dict = collection_auth.find_one({"user_email": user_email})
    if user_dict:
        return UserInDB(**user_dict)

def authenticate_user(user_email: str, password: str):
    """
    this function is used to verify user with username and password
    """
    user = get_user(user_email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def verify_password(plain_password, hashed_password):
    """
    compares hashes of input password and OG password
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    when user verified, creates encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    will return credentials of current enabled user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
        token_data = TokenData(user_email=user_email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(user_email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """
    will return user if is enabled
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



from fastapi import FastAPI
auth_router = APIRouter()

@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestFormEmail, Depends()],
) -> Token:
    user = authenticate_user(form_data.user_email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/register_user")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestFormEmail, Depends()],
) -> Token:
    user = authenticate_user(form_data.user_email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@auth_router.get("/users/me/", response_model=AuthUser)
async def read_users_me(
    current_user: Annotated[AuthUser, Depends(get_current_active_user)],
):
    return current_user


#### register

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str


from fastapi import FastAPI, HTTPException, status
from pymongo.errors import DuplicateKeyError



@auth_router.post("/register_user", response_model=AuthUser, status_code=status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate):
    user_dict = collection_auth.find_one({"user_email": user_create.email})
    if user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = get_password_hash(user_create.password)
    new_user = UserInDB(email=user_create.email, hashed_password=hashed_password)

    try:
        collection_auth.insert_one(new_user.dict())
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return new_user

