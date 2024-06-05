"""
original author: Dominik Cedro
created: 2024-05-29
license: BSD 3.0
description: This module contains model for Users collection
"""
from pydantic import BaseModel
from typing import List, Optional

from models.evaluations import Stroop, DigitSubstitution, TrailMaking


class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    version: int
    email: str
    stroop: Optional[List[Stroop]] = []
    digit_substitution: Optional[List[DigitSubstitution]] = []
    trail_making: Optional[List[TrailMaking]] = []