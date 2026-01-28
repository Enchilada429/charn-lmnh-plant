"""Test fixtures for the pipeline."""

# pylint:skip-file

import pytest


@pytest.fixture
def test_plant_data() -> list[dict]:
    return [
        {
            "botanist": {
                "email": "anna.davis@lnhm.co.uk",
                "name": "Anna Davis",
                "phone": "(601)561-8163x5240"
            },
            "images": {
                "license": 451,
                "license_name": "Universal",
                "license_url": "license.com",
                "medium_url": "medium.com",
                "original_url": "original.com",
                "regular_url": "regular.com",
                "small_url": "small.com",
                "thumbnail": "thumbnail.com"
            },
            "last_watered": "2026-01-27T14:47:07",
            "name": "Bird of paradise",
            "origin_location": {
                "city": "South Tina",
                "country": "United Arab Emirates",
                "latitude": "-60.9363685",
                "longitude": "-152.763324"
            },
            "plant_id": 8,
            "recording_taken": "2026-01-27T16:04:39.600475",
            "scientific_name": [
                "Heliconia schiedeana 'Fire and Ice'"
            ],
            "soil_moisture": 95.0,
            "temperature": 16.0
        },
        {
            "botanist": {
                "email": "virginia.phillips@lnhm.co.uk",
                "name": "Virginia Phillips",
                "phone": "8273002266"
            },
            "last_watered": "2026-01-27T14:38:15",
            "name": "Cactus",
            "origin_location": {
                "city": "Gambleshire",
                "country": "Nauru",
                "latitude": "-42.9962205",
                "longitude": "-123.053507"
            },
            "plant_id": 9,
            "recording_taken": "2026-01-27T16:08:05.093205",
            "scientific_name": [
                "Pereskia grandifolia"
            ],
            "soil_moisture": 94.99991354267162,
            "temperature": 15.48521577170627
        }
    ]
