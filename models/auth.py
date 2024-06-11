"""
original author: Dominik Cedro
created:
"""
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ValidationError, field_validator
from models.evaluations import Stroop, DigitSubstitution, TrailMaking

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserRegisterRequest(BaseModel):
    first_name: str
    last_name: str
    version: int
    email: EmailStr
    password: str
