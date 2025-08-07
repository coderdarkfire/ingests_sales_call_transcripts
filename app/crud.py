from datetime import datetime
from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app import models


def get_calls(
    db: Session,
    limit: int = 10,
    offset: int = 0,
    agent_id: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    min_sentiment: Optional[float] = None,
    max_sentiment: Optional[float] = None,
):
    filters = []

    if agent_id:
        filters.append(models.Call.agent_id == agent_id)
    if from_date:
        filters.append(models.Call.start_time >= from_date)
    if to_date:
        filters.append(models.Call.start_time <= to_date)
    if min_sentiment is not None:
        filters.append(models.Call.customer_sentiment_score >= min_sentiment)
    if max_sentiment is not None:
        filters.append(models.Call.customer_sentiment_score <= max_sentiment)

    return (
        db.query(models.Call).filter(and_(*filters)).offset(offset).limit(limit).all()
    )
