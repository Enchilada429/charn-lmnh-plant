"""This script will run simple tests for the functionality within extract.py."""

from unittest.mock import AsyncMock, patch

import pytest
import aiohttp

from extract import PLANT_ENDPOINT, get_plant_data, get_all_plants_data


@pytest.mark.asyncio
async def test_get_plant_data_with_patch():
    expected_payload = {"plant_id": 1, "name": "Carnation"}

    with patch("aiohttp.ClientSession.get", new_callable=AsyncMock) as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = expected_payload
        
        mock_manager = AsyncMock()
        
        mock_manager.return_value.__aenter__.return_value = mock_response
        mock_manager.return_value.__aexit__.return_value = None

        mock_response.return_value = mock_response

        async with aiohttp.ClientSession() as session:
            result = await get_plant_data(session, plant_id=1)

    assert result == expected_payload
    mock_get.assert_called_once_with(PLANT_ENDPOINT + "1")

@patch.get_plant_data
@pytest.mark.asyncio
async def test_get_all_plants_data(loaded_data):
    with patch("aiohttp.ClientSession.get", new_callable=AsyncMock) as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = loaded_data
        
        mock_manager = AsyncMock()
        
        mock_manager.return_value.__aenter__.return_value = mock_response
        mock_manager.return_value.__aexit__.return_value = AsyncMock()
        
        
        mock_get.return_value = mock_response

        async with aiohttp.ClientSession() as session:
            result = await get_all_plants_data(5)

    assert result == loaded_data
    

@pytest.mark.asyncio
async def test_fetch_data(loaded_data):
    assert loaded_data[0]["plant_id"] == 1
    