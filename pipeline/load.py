"""Script for uploading the cleaned data to the RDS (SQL Server)."""

from logging import getLogger, basicConfig, INFO
from os import environ as ENV, _Environ

import pyodbc
from dotenv import load_dotenv

from extract import extract
from transform import transform_data


logger = getLogger(__name__)


def get_db_connection(config: _Environ):
    """Create and return a SQL Server connection."""
    conn_str = (
        f"DRIVER={{{config['DB_DRIVER']}}};"
        f"SERVER={config['DB_HOST']},{config['DB_PORT']};"
        f"DATABASE={config['DB_NAME']};"
        f"UID={config['DB_USERNAME']};"
        f"PWD={config['DB_PASSWORD']};"
        f"Encrypt=no;"
    )

    logger.info("Connecting to SQL Server.")
    conn = pyodbc.connect(conn_str)
    logger.info("Connection established.")

    return conn


def upload_recording_to_database(conn, recording) -> None:
    """Uploads formatted recording data to the DB."""
    logger.info(f"Starting upload of {len(recording)} recording.")

    recording_to_insert = []
    for _, row in recording.iterrows():
        recording_to_insert.append(
            (
                row["plant_id"], row["botanist_id"], row["origin_location_id"], row["last_watered"], row[
                    "image_id"], row["recording_taken"], row["soil_moisture"], row["temperature"],
            )
        )

    insert_query = """INSERT INTO recording (plant_id, botanist_id, origin_location_id, last_watered,
        image_id, recording_taken, soil_moisture, temperature
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """

    with conn.cursor() as curs:
        curs.fast_executemany = True
        curs.executemany(insert_query, recording_to_insert)

    conn.commit()
    logger.info(
        f"Successfully inserted {len(recording_to_insert)} recording data.")


if __name__ == "__main__":

    basicConfig(level=INFO)

    load_dotenv()

    extracted_data = extract()
    df_transformed = transform_data(extracted_data)

    conn = get_db_connection(ENV)
    try:
        upload_recording_to_database(conn, df_transformed)
    finally:
        conn.close()
