from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CallBase(BaseModel):
    agent_id: str
    customer_id: str
    language: str
    start_time: datetime
    duration_seconds: int
    transcript: str

class CallCreate(CallBase):
    pass

class CallOut(CallBase):
    id: str
    agent_talk_ratio: Optional[float]
    customer_sentiment_score: Optional[float]

    class Config:
        orm_mode = True
