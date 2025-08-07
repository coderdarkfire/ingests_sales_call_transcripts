import pytest


@pytest.mark.asyncio
async def test_list_calls(async_client):
    response = await async_client.get("/api/v1/calls")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "calls" in data
    if data["calls"]:
        global first_call_id
        first_call_id = data["calls"][0]["id"]  # Store for use in next test


@pytest.mark.asyncio
async def test_get_call_by_id(async_client):
    response = await async_client.get(f"/api/v1/calls/{first_call_id}")
    assert response.status_code == 200
    data = response.json()
    assert "transcript" in data
    assert data["id"] == first_call_id
