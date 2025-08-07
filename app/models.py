from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class CallLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    call_id: str
    agent_id: int
    customer_id: int
    language: str
    call_time: datetime
    duration: int
    transcript: str
    status: str
    agent_talk_ratio: float
    customer_sentiment_score: float
    embedding: str

