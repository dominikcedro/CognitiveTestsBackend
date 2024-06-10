"""
original author: Dominik Cedro
created: 2024-05-29
license: BSD 3.0
description: This module contains model for Users collection
"""
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ValidationError, field_validator
from models.evaluations import Stroop, DigitSubstitution, TrailMaking


class User(BaseModel):
    first_name: str
    last_name: str
    version: int
    email: EmailStr