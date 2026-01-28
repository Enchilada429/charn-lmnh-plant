"""These are basic data fixtures for testing."""

import pytest
import asyncio
import pytest_asyncio

@pytest.fixture
def fake_api_data():
    """Returns fake API data."""
    return [
        {"plant_id": 1, "name": "Carnation"},
        {"plant_id": 2, "name": "Rose"},
        {"plant_id": 3, "name": "Lily"},
        {"plant_id": 4, "name": "Waterlily"},
        {"plant_id": 5, "name": "Baby Breath"}
    ]
    

@pytest_asyncio.fixture
async def loaded_data():
    await asyncio.sleep(5)
    return [
        {"plant_id": 1, "name": "Carnation"},
        {"plant_id": 2, "name": "Rose"},
        {"plant_id": 3, "name": "Lily"},
        {"plant_id": 4, "name": "Waterlily"},
        {"plant_id": 5, "name": "Baby Breath"}
    ]