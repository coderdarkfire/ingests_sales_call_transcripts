# seed_data.py

import datetime
import random

from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from app.database import engine
from app.models import CallLog

#  Ensure table exists
SQLModel.metadata.create_all(engine)

# Create DB session
session = Session(bind=engine)

# Sample data
call_logs = [
    CallLog(
        call_id=f"CALL{random.randint(10000, 99999)}",
        agent_id=random.randint(1, 5),
        customer_id=random.randint(100, 110),
        call_time=datetime.datetime(2025, 8, 1, 14, 30),
        duration=180,
        status="outgoing",
    ),
    CallLog(
        call_id=f"CALL{random.randint(10000, 99999)}",
        agent_id=random.randint(1, 5),
        customer_id=random.randint(100, 110),
        call_time=datetime.datetime(2025, 8, 2, 16, 45),
        duration=60,
        status="incoming",
    ),
    CallLog(
        call_id=f"CALL{random.randint(10000, 99999)}",
        agent_id=random.randint(1, 5),
        customer_id=random.randint(100, 110),
        call_time=datetime.datetime(2025, 8, 3, 10, 15),
        duration=240,
        status="missed",
    ),
]

# Add and commit to DB
session.add_all(call_logs)
session.commit()
session.close()

print(" Sample call log data seeded successfully!")
