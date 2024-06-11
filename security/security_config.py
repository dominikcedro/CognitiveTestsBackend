from datetime import timedelta, datetime, timezone
from typing import Union

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel

### PASSWORDS MANAGEMENT - hashing

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """
    this function utilizes CryptContext bcrypt to hash parameter "password"
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    compares hashes of input password and OG password
    """
    return pwd_context.verify(plain_password, hashed_password)

### TOKENS

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str



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