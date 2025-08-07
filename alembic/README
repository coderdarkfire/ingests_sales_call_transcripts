# 📞 Call Analytics Microservice

This microservice ingests sales call transcripts, performs AI-based analysis (embeddings, sentiment, and agent talk ratio), and exposes insights through a REST API built with **FastAPI** and **SQLite** (PostgreSQL-compatible via SQLAlchemy).

---

## 🚀 Features

- Async ingestion of synthetic call transcripts (Faker-generated)
- SQLAlchemy + Alembic migrations
- Embedding & sentiment analysis using Hugging Face + sentence-transformers
- REST APIs for:
  - Listing calls with filters
  - Call details
  - Similar call recommendations
  - Agent analytics leaderboard
- Easily extendable (JWT, WebSocket, background tasks)

---

## 🧠 Tech Stack

- FastAPI
- SQLAlchemy + Alembic
- SQLite (can switch to PostgreSQL)
- Hugging Face Transformers
- Sentence Transformers
- Uvicorn
- Pydantic

---

## 📦 Project Structure


call_analytics/
│
├── app/
│ ├── models.py # SQLAlchemy + Pydantic models
│ ├── database.py # DB session setup
│ ├── routes.py # All API endpoints
│ └── init.py
│
├── alembic/ # Alembic migrations
│
├── process_raw_data.py # Script to ingest & analyze calls
├── requirements.txt # Project dependencies
├── call_analytics.db # SQLite DB (auto-created)
├── main.py # FastAPI app entrypoint
└── README.md # You're here!

---

## ⚙️ Setup Instructions

### 1. 🐍 Create a virtual environment
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows


### 2. 📦 Install dependencies

pip install -r requirements.txt

### 3. 🛠️ Run Alembic migrations

alembic upgrade head
This creates the database schema.

### 4. 📥 Ingest sample call transcripts

python process_raw_data.py

This will:
- Generate 200 fake call records
- Compute embeddings and sentiment
- Populate the database

### 5. 🚀 Run the FastAPI server

uvicorn main:app --reload

Visit the API docs: http://127.0.0.1:8000/docs

---

## 🧪 Sample API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /calls   | List calls with filters |
| GET    | /calls/{call_id} | Get call by ID |
| GET    | /calls/{call_id}/recommendations | Similar calls + coaching nudges |
| GET    | /analytics/agents | Agent-wise leaderboard |

---


## 🧠 License & Credits

- Faker – for fake data
- Sentence Transformers – for embeddings
- Hugging Face – for sentiment analysis