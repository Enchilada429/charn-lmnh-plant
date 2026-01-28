"""Script for uploading the cleaned data to the RDS (SQL Server)."""

import logging
from os import environ as ENV

import pyodbc
from dotenv import load_dotenv

from extract import extract_data
from transform import transform_data


logging.basicConfig(level=logging.INFO)


def handler(event=None, context=None):
    """Create and return a SQL Server connection."""
    conn_str = (
        f"DRIVER={{{ENV['DB_DRIVER']}}};"
        f"SERVER={ENV['DB_HOST']},{ENV['DB_PORT']};"
        f"DATABASE={ENV['DB_NAME']};"
        f"UID={ENV['DB_USERNAME']};"
        f"PWD={ENV['DB_PASSWORD']};"
        f"Encrypt=no;"
    )

    logging.info("Connecting to SQL Server")
    conn = pyodbc.connect(conn_str)
    logging.info("Connection established")

    return conn


def upload_recording_to_database(conn, recording) -> None:
    """Uploads formatted recording data to the DB."""
    logging.info("Starting upload of %d recording", len(recording))

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
    logging.info("Successfully inserted %d recording data.",
                len(recording_to_insert))



if __name__ == "__main__":
    load_dotenv()

    data = extract_data()
    df_transformed = transform_data(data)

    conn = handler()
    try:
        upload_recording_to_database(conn, df_transformed)
    finally:
        conn.close()
