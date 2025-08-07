from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import CallLog
from app.database import SessionLocal
from sqlmodel import select
from fastapi import Path
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import random
from fastapi.responses import JSONResponse
from sqlalchemy import func
from app.models import CallLog
# from app.models import CallLog as CallLogModel, CallLogResponse
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from sqlalchemy.orm import Session
from sqlmodel import select
from typing import List, Optional
from app.models import CallLog
from app.database import SessionLocal


router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.get("/calls", response_model=List[CallLog])
# def get_calls(
#     limit: int = Query(10, ge=1),
#     offset: int = Query(0, ge=0),
#     agent_id: Optional[int] = None,
#     db: Session = Depends(get_db)
    
# ):
#     query = select(CallLog)
#     if agent_id:
#         query = query.where(CallLog.agent_id == agent_id)
#     calls = db.exec(query.offset(offset).limit(limit)).all()
#     return calls

@router.get("/calls", response_model=List[CallLog])
def get_calls(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    agent_id: Optional[int] = None,
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    min_sentiment: Optional[float] = Query(None, ge=-1.0, le=1.0),
    max_sentiment: Optional[float] = Query(None, ge=-1.0, le=1.0),
    db: Session = Depends(get_db)
):
    query = select(
        CallLog.id,
        CallLog.call_id,
        CallLog.agent_id,
        # CallLog.call_time,
        CallLog.customer_sentiment_score
    )

    if agent_id:
        query = query.where(CallLog.agent_id == agent_id)
    if from_date:
        query = query.where(CallLog.call_time >= from_date)
    if to_date:
        query = query.where(CallLog.call_time <= to_date)
    if min_sentiment is not None:
        query = query.where(CallLog.customer_sentiment_score >= min_sentiment)
    if max_sentiment is not None:
        query = query.where(CallLog.customer_sentiment_score <= max_sentiment)

    results = db.execute(query.offset(offset).limit(limit)).all()

    # Map to list of dicts
    calls = [
        {
            "id": r.id,
            "call_id": r.call_id,
            "agent_id": r.agent_id,
            "customer_sentiment_score": r.customer_sentiment_score
        }
        for r in results
    ]

    return JSONResponse(content={"calls": calls})


@router.get("/calls/{call_id}", response_model=CallLog)
def get_call_by_id(
    call_id: int = Path(..., description="The ID of the call to retrieve"),
    db: Session = Depends(get_db)
):
    call = db.get(CallLog, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call

def get_static_coaching_nudges():
    nudges = [
        "Try using more open-ended questions.",
        "Slow down your speaking pace to build rapport.",
        "Practice active listening to uncover customer needs."
    ]
    return random.sample(nudges, 3)


@router.get("/calls/{call_id}/recommendations")
def get_call_recommendations(call_id: str, db: Session = Depends(get_db)):
    base_call = db.query(CallLog).filter(CallLog.call_id == call_id).first()
    if not base_call:
        raise HTTPException(status_code=404, detail="Call not found")

    if not base_call.embedding:
        raise HTTPException(status_code=400, detail="Embedding not available for base call")

    # Convert the embedding string to numpy array
    try:
        base_vector = np.array(json.loads(base_call.embedding)).reshape(1, -1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing embedding: {str(e)}")

    # Get all other calls
    all_calls = db.query(CallLog).filter(CallLog.call_id != call_id).all()

    similarities = []
    for call in all_calls:
        try:
            if call.embedding:
                other_vector = np.array(json.loads(call.embedding)).reshape(1, -1)
                sim = cosine_similarity(base_vector, other_vector)[0][0]
                similarities.append((call.call_id, sim))
        except Exception:
            continue

    # Sort by similarity
    top_5 = sorted(similarities, key=lambda x: x[1], reverse=True)[:5]

    return {
        "similar_calls": [{"call_id": cid, "similarity": round(score, 4)} for cid, score in top_5],
        "coaching_nudges": get_static_coaching_nudges()
    }
    
    
@router.get("/analytics/agents")
def get_agent_analytics(db: Session = Depends(get_db)):
    results = db.query(
        CallLog.agent_id,
        func.avg(CallLog.customer_sentiment_score).label("avg_sentiment"),
        func.avg(CallLog.agent_talk_ratio).label("avg_talk_ratio"),
        func.count(CallLog.id).label("call_count")
    ).group_by(CallLog.agent_id).all()

    leaderboard = [
        {
            "agent_id": row.agent_id,
            "avg_sentiment": round(row.avg_sentiment, 3) if row.avg_sentiment is not None else None,
            "avg_talk_ratio": round(row.avg_talk_ratio, 3) if row.avg_talk_ratio is not None else None,
            "call_count": row.call_count
        }
        for row in results
    ]

    return {"leaderboard": leaderboard}



