"""
original author: Dominik Cedro
created: 2024-05-29
license: BSD 3.0
description: This module contains model for Users collection
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ValidationError, field_validator
from models.evaluations import Stroop, DigitSubstitution, TrailMaking

class TestStats(BaseModel):
    top_score: Optional[int] = None
    mean_total_score: Optional[float] = None
    mean_mistake_count: Optional[float] = None
    last_test_date: Optional[datetime] = None
    test_count: Optional[int] = None

class UserStats(BaseModel):
    stroop: Optional[TestStats] = None
    digit_substitution: Optional[TestStats] = None
    trail_making: Optional[TestStats] = None

class User(BaseModel):
    first_name: str
    last_name: str
    version: int
    email: EmailStr
    user_stats: Optional[UserStats] = None

class UpdateUserRequest(BaseModel):
    first_name: str
    last_name: str
    version: int
    email: EmailStr
    password: str


