from fastapi import FastAPI
from app.routes import router as call_router

app = FastAPI()

app.include_router(call_router, prefix="/api/v1")
