"""Script for executing the entire ETL pipeline."""

from os import environ as ENV

from extract import extract
from transform import transform_data
from load import get_db_connection, upload_recording_to_database


if __name__ == "__main__":
    ...
