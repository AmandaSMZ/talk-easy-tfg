from pydantic import BaseModel
from typing import List

class TagRequest(BaseModel):
    text: str
    labels: List[str]

class TagProbability(BaseModel):
    label: str
    score: float

class TagResponse(BaseModel):
    predicted_labels: List[str]
    probabilities: List[TagProbability]