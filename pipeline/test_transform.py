"""Testing transform.py"""

# pylint:skip-file

import pandas as pd
from datetime import datetime

from transform import build_dataframe, convert_datatypes, drop_outliers


def test_build_dataframe_valid_columns(test_plant_data):
    test_df = build_dataframe(test_plant_data)

    needed_columns = [
        "plant_id",
        "plant_name",
        "scientific_name",
        "botanist_name",
        "email",
        "phone",
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
        "email": ["anna.davis@lnhm.co.uk"],
        "phone": ["(601)561-8163x5240"],
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
    test_df = pd.DataFrame(data={
        "latitude": ["-60.9363685"],
        "longitude": ["-152.763324"],
        "last_watered": ["2026-01-27T14:47:07"],
        "recording_taken": ["2026-01-27T16:04:39.600475"],
        "soil_moisture": [95.0],
        "temperature": [16.0],
        "scientific_name": [None],
        "license": [None],
        "license_url": [None],
        "license_name": [None],
        "thumbnail": [None],
        "email": [None],
        "phone": [None],
    })

    converted_df = convert_datatypes(test_df)

    assert all(converted_df["latitude"].map(
        lambda val: isinstance(val, float)))
    assert all(converted_df["longitude"].map(
        lambda val: isinstance(val, float)))
    assert all(converted_df["last_watered"].map(
        lambda val: isinstance(val, pd.Timestamp)))
    assert all(converted_df["recording_taken"].map(
        lambda val: isinstance(val, pd.Timestamp)))
    assert all(converted_df["soil_moisture"].map(
        lambda val: isinstance(val, float)))
    assert all(converted_df["temperature"].map(
        lambda val: isinstance(val, float)))

    assert converted_df.loc[0, "scientific_name"] == "None"
    assert converted_df.loc[0, "license"] == 0
    assert converted_df.loc[0, "license_url"] == "None"
    assert converted_df.loc[0, "license_name"] == "None"
    assert converted_df.loc[0, "thumbnail"] == "None"
    assert converted_df.loc[0, "email"] == "None"
    assert converted_df.loc[0, "phone"] == "None"


def test_drop_outliers_valid():
    test_df = pd.DataFrame(data={
        "soil_moisture": [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 50.0],
        "temperature": [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 50.0]
    })

    no_outlier_df = drop_outliers(test_df)

    difference_df = pd.concat(
        [test_df.head(10), no_outlier_df]).drop_duplicates(keep=False)

    assert difference_df.empty
