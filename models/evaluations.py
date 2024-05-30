from pydantic import BaseModel


class Evaluation(BaseModel):
    type: str
    description: str

