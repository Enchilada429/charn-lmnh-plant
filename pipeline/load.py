"""Script for uploading the cleaned data to the RDS (SQL Server)."""

import pyodbc
from os import environ as ENV
from dotenv import load_dotenv
import logging
from pyodbc import execute_values


def handler(event=None, context=None):
    conn_str = (
        f"DRIVER={{{ENV['DB_DRIVER']}}};"
        f"SERVER={ENV['DB_HOST']},{ENV['DB_PORT']};"
        f"DATABASE={ENV['DB_NAME']};"
        f"UID={ENV['DB_USERNAME']};"
        f"PWD={ENV['DB_PASSWORD']};"
        f"Encrypt=no;"
    )

    conn = pyodbc.connect(conn_str)

    with conn.cursor() as cur:
        q = """
        
        """
        cur.execute(q)
        data = cur.fetchall()

    conn.close()

    return


def upload_recording_to_database(conn, recording) -> None:
    """Uploads formatted recording data to the DB."""
    logging.info("Starting upload of %d recording", len(recording))

    recording_to_insert = []
    for _, row in recording.iterrows():
        recording_to_insert.append(
            (row["plant_id"], row["botanist_id"], row["origin_location_id"], row["last_watered"], row["image_id"], row["recording_taken"], row["soil_moisture"], row["temperature"]))
    insert_query = """INSERT INTO recording (plant_id, botanist_id, origin_location_id, last_watered, image_id, recording_taken, soil_moisture, temperature)
                        VALUES ?;"""
    with conn.cursor() as curs:
        execute_values(curs, insert_query, (recording_to_insert,))
    conn.commit()
    logging.info(
        "Successfully inserted %d rating records.",
        len(recording_to_insert)
    )
    logging.info(
        "Successfully inserted rows."
    )


if __name__ == "__main__":
    load_dotenv()
    print(handler())
