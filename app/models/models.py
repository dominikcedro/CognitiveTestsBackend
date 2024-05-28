
from typing import Union, Annotated
from pydantic import BaseModel


class Token(BaseModel):
    """
    token class represents the attributes of token
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    tokenData class
    """
    username: Union[str, None] = None

class User(BaseModel):
    """
    user represents data stored in users collection for each registered user
    """
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

class UserCreate(User):
    password: str