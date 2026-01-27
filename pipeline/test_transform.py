"""Testing transform.py"""

# pylint:skip-file

import pandas as pd
from datetime import datetime

from transform import build_dataframe, convert_datatypes


def test_build_dataframe_valid_columns(test_plant_data):
    test_df = build_dataframe(test_plant_data)

    needed_columns = [
        "plant_id",
        "plant_name",
        "scientific_name",
        "botanist_name",
        "botanist_email",
        "botanist_phone",
        "origin_city",
        "origin_country",
        "latitude",
        "longitude",
        "license",
        "license_name",
        "license_url",
        "thumbnail",
        "last_watered",
        "recording_taken",
        "soil_moisture",
        "temperature"
    ]

    assert set(test_df.columns) == set(needed_columns)


def test_build_dataframe_valid_df(test_plant_data):
    test_df = build_dataframe(test_plant_data).head(1)

    actual_df = pd.DataFrame(data={
        "plant_id": [8],
        "plant_name": ["Bird of paradise"],
        "scientific_name": ["Heliconia schiedeana 'Fire and Ice'"],
        "botanist_name": ["Anna Davis"],
        "botanist_email": ["anna.davis@lnhm.co.uk"],
        "botanist_phone": ["(601)561-8163x5240"],
        "origin_city": ["South Tina"],
        "origin_country": ["United Arab Emirates"],
        "latitude": ["-60.9363685"],
        "longitude": ["-152.763324"],
        "license": [451],
        "license_name": ["Universal"],
        "license_url": ["license.com"],
        "thumbnail": ["thumbnail.com"],
        "last_watered": ["2026-01-27T14:47:07"],
        "recording_taken": ["2026-01-27T16:04:39.600475"],
        "soil_moisture": [95.0],
        "temperature": [16.0]
    })

    difference_df = pd.concat([test_df, actual_df]).drop_duplicates(keep=False)

    assert difference_df.empty


def test_convert_datatypes_valid():
    test_df = pd.DataFrame({
        "latitude": ["-60.9363685"],
        "longitude": ["-152.763324"],
        "last_watered": ["2026-01-27T14:47:07"],
        "recording_taken": ["2026-01-27T16:04:39.600475"],
        "soil_moisture": [95.0],
        "temperature": [16.0]
    })
    print(test_df.dtypes)
    converted_df = convert_datatypes(test_df)

    assert all(converted_df["latitude"].map(
        lambda val: isinstance(val, float)))
    assert all(converted_df["longitude"].map(
        lambda val: isinstance(val, float)))
    assert all(converted_df["last_watered"].map(
        lambda val: isinstance(val, datetime)))
    assert all(converted_df["recording_taken"].map(
        lambda val: isinstance(val, datetime)))
    assert all(converted_df["soil_moisture"].map(
        lambda val: isinstance(val, float)))
    assert all(converted_df["temperature"].map(
        lambda val: isinstance(val, float)))
