from typing import Optional

from pydantic import BaseModel


class Evaluation(BaseModel):
    test_id: int
    user_id: int
    type: str
    version: int
    score: int
    date_taken: str
    custom_field_1: Optional[str]
    custom_field_2: Optional[str]


