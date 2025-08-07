import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app  # replace with the actual path to your FastAPI app


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
