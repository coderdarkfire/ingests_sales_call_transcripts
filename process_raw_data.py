import os
import json
import random
import asyncio
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy.orm import Session
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from app.database import SessionLocal
from app.models import CallLog
from sqlmodel import SQLModel
from sqlalchemy.orm import Session
from app.models import CallLog
from app.database import engine

from datetime import datetime, timedelta
import random

# ✅ Ensure table exists
SQLModel.metadata.create_all(engine)


# Setup
data_dir = "data/raw_calls"
os.makedirs(data_dir, exist_ok=True)
fake = Faker()

sentiment_analyzer = pipeline("sentiment-analysis")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

AGENT_IDS = [1, 2, 3, 4, 5]
CUSTOMER_IDS = list(range(100, 150))
STATUSES = ["completed", "missed", "failed"]
LANGUAGES = ["en", "es", "fr"]


def generate_transcript():
    transcript = []
    for _ in range(random.randint(5, 15)):
        speaker = random.choice(["Agent", "Customer"])
        sentence = fake.sentence(nb_words=random.randint(4, 10))
        transcript.append(f"{speaker}: {sentence}")
    return "\n".join(transcript)


async def save_transcript_json(call_data, index):
    filename = f"call_{index}.json"
    filepath = os.path.join(data_dir, filename)
    async with asyncio.Lock():
        with open(filepath, "w") as f:
            json.dump(call_data, f, indent=2)


def create_fake_call(index):
    start_time = datetime.utcnow() - timedelta(days=random.randint(0, 90))
    duration = random.randint(30, 600)
    return {
        "call_id": f"CALL{10000 + index}",
        "agent_id": random.choice(AGENT_IDS),
        "customer_id": random.choice(CUSTOMER_IDS),
        "language": random.choice(LANGUAGES),
        "start_time": start_time.isoformat(),
        "duration_seconds": duration,
        "transcript": generate_transcript(),
        "status": random.choice(STATUSES)
    }


async def ingest_calls(n=200):
    tasks = []
    for i in range(n):
        call_data = create_fake_call(i)
        tasks.append(save_transcript_json(call_data, i))
    await asyncio.gather(*tasks)
    return n


def calculate_agent_talk_ratio(transcript: str) -> float:
    agent_words = sum(len(line.split()) for line in transcript.splitlines() if line.startswith("Agent:"))
    customer_words = sum(len(line.split()) for line in transcript.splitlines() if line.startswith("Customer:"))
    total_words = agent_words + customer_words
    return round(agent_words / total_words, 2) if total_words > 0 else 0.0


def analyze_sentiment(transcript: str) -> float:
    customer_lines = [line[9:] for line in transcript.splitlines() if line.startswith("Customer:")]
    if not customer_lines:
        return 0.0
    customer_text = " ".join(customer_lines)
    result = sentiment_analyzer(customer_text)[0]
    return round(result["score"] if result["label"] == "POSITIVE" else -result["score"], 2)


def process_and_store_to_db():
    db: Session = SessionLocal()
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r") as f:
            data = json.load(f)

        if db.query(CallLog).filter_by(call_id=data["call_id"]).first():
            continue

        agent_talk_ratio = calculate_agent_talk_ratio(data["transcript"])
        sentiment_score = analyze_sentiment(data["transcript"])
        embedding = embedder.encode(data["transcript"]).tolist()

        call = CallLog(
            call_id=data["call_id"],
            agent_id=data["agent_id"],
            customer_id=data["customer_id"],
            language=data["language"],
            call_time=datetime.fromisoformat(data["start_time"]),
            duration=data["duration_seconds"],
            transcript=data["transcript"],
            status=data["status"],
            agent_talk_ratio=agent_talk_ratio,
            customer_sentiment_score=sentiment_score,
            embedding=json.dumps(embedding)
        )
        db.add(call)

    db.commit()
    db.close()


# Run full pipeline
if __name__ == "__main__":
    asyncio.run(ingest_calls(200))
    process_and_store_to_db()
