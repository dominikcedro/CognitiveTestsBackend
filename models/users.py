"""
original author: Dominik Cedro
created: 2024-05-29
license: BSD 3.0
description: This module contains model for Users collection
"""
from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    version: int
    email: str
    test_ids: Optional[List[int]] = []

