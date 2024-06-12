"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: This module contains main fastAPI app that runs backend for CognitiveTests mobile app.
"""
from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class Evaluation(BaseModel):
    test_id: int
    user_id: int
    type: str
    version: int
    score: int
    date_taken: str
    custom_field_1: Optional[str]
    custom_field_2: Optional[str]


class Stroop(BaseModel):
    stroop_id: int
    version: int
    datetime: datetime
    mistake_count: int
    total_score: int


class DigitSubstitution(BaseModel):
    digit_sub_id: int
    version: int
    datetime: datetime
    time: int
    mistake_count: int
    total_score: int


class TrailMaking(BaseModel):
    trail_making_id: int
    version: int
    datetime: datetime
    time: int
    mistake_count: int
    total_score: int
