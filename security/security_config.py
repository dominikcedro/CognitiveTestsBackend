from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

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