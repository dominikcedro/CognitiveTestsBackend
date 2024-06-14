"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: This module contains main fastAPI app that runs backend for CognitiveTests mobile app.
"""
from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class Stroop(BaseModel):
    stroop_id: int
    version: int
    datetime: datetime
    mistake_count: int
    total_score: int

class PostStroopRequest(BaseModel):
    datetime: datetime
    mistake_count: int
    # total_score: int


class DigitSubstitution(BaseModel):
    digit_sub_id: int
    version: int
    datetime: datetime
    mistake_count: int
    correct_answers: int
    total_score: int

class PostDigitSubstitutionRequest(BaseModel):
    datetime: datetime
    mistake_count: int
    correct_answers: int
    # total_score: int


class TrailMaking(BaseModel):
    trail_making_id: int
    version: int
    datetime: datetime
    time: int
    mistake_count: int
    total_score: int


class PostTrailMakingRequest(BaseModel):
    datetime: datetime
    time: int
    mistake_count: int


class GetAllEvaluationsResponse(BaseModel):
    stroop: Optional[list[Stroop]] = None
    digit_substitution: Optional[list[DigitSubstitution]]=None
    trail_making: Optional[list[TrailMaking]]=None