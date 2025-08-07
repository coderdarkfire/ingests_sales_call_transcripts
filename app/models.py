from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class CallLog(SQLModel, table=True):  # type: ignore
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
