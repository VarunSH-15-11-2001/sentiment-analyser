from pydantic import BaseModel, Field
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to analyze")

class Score(BaseModel):
    label: str
    score: float

class AnalyzeResponse(BaseModel):
    label: str
    scores: List[Score]
    model: str
    latency_ms: float

class BatchItem(BaseModel):
    id: str
    text: str

class BatchRequest(BaseModel):
    items: List[BatchItem]

class BatchResponseItem(BaseModel):
    id: str
    label: str
    scores: List[Score]

class BatchResponse(BaseModel):
    model: str
    results: List[BatchResponseItem]