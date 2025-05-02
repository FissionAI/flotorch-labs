from pydantic import BaseModel
from typing import  List

class ModelInfo(BaseModel):
    label: str
    value: str
    service: str


class Conversation(BaseModel):
    question: str
    models: List[ModelInfo]
