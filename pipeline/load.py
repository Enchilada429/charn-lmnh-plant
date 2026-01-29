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


def get_or_create_country_id(cur, country_name: str) -> int:
    """Gets or creates country_id"""
    cur.execute(
        "SELECT country_id FROM beta.country WHERE country_name = ?;",
        (country_name,),
    )
    row = cur.fetchone()
    if row:
        return int(row[0])

    cur.execute(
        "INSERT INTO beta.country (country_name) VALUES (?);",
        (country_name,),
    )

    cur.execute(
        "SELECT country_id FROM beta.country WHERE country_name = ?;",
        (country_name,),
    )
    return int(cur.fetchone()[0])


def get_or_create_botanist_id(cur, name, email, phone):
    """Gets or creates botanist_id"""
    cur.execute(
        "SELECT botanist_id FROM beta.botanist WHERE email = ?;",
        (email,),
    )
    row = cur.fetchone()
    if row:
        return int(row[0])

    cur.execute(
        "INSERT INTO beta.botanist (botanist_name, email, phone) VALUES (?, ?, ?);",
        (name, email, phone),
    )

    cur.execute(
        "SELECT botanist_id FROM beta.botanist WHERE email = ?;",
        (email,),
    )
    return int(cur.fetchone()[0])


def get_or_create_plant_id(cur, common_name: str, scientific_name: str | None) -> int:
    """Gets or creates plant_id"""
    cur.execute(
        "SELECT plant_id FROM beta.plant WHERE common_name = ?;",
        (common_name,),
    )
    row = cur.fetchone()
    if row:
        return int(row[0])

    cur.execute(
        "INSERT INTO beta.plant (common_name, scientific_name) VALUES (?, ?);",
        (common_name, scientific_name),
    )

    cur.execute(
        "SELECT plant_id FROM beta.plant WHERE common_name = ?;",
        (common_name,),
    )
    return int(cur.fetchone()[0])


def get_or_create_image_id(cur, license: int, license_name: str, license_url: str, thumbnail: str | None) -> int:
    """Gets or creates image_id"""
    cur.execute(
        "SELECT image_id FROM beta.plant_image WHERE licence = ?;",
        (license,),
    )
    row = cur.fetchone()
    if row:
        return int(row[0])

    cur.execute(
        "INSERT INTO beta.plant_image (licence, licence_name, licence_url, thumbnail) VALUES (?, ?, ?, ?);",
        (license, license_name, license_url, thumbnail,),
    )

    cur.execute(
        "SELECT image_id FROM beta.plant_image WHERE licence = ?;",
        (license,),
    )
    return int(cur.fetchone()[0])


def get_or_create_origin_location_id(cur, city: str, country_id: int, longitude, latitude) -> int:
    """Gets or creates location_id"""
    cur.execute(
        """
        SELECT origin_location_id
        FROM beta.origin_location
        WHERE origin_city_name = ? AND country_id = ?;
        """,
        (city, country_id),
    )
    row = cur.fetchone()
    if row:
        return int(row[0])

    cur.execute(
        """
        INSERT INTO beta.origin_location (origin_city_name, country_id, longitude, latitude)
        VALUES (?, ?, ?, ?);
        """,
        (city, country_id, longitude, latitude),
    )

    cur.execute(
        """
        SELECT origin_location_id
        FROM beta.origin_location
        WHERE origin_city_name = ? AND country_id = ?;
        """,
        (city, country_id),
    )
    return int(cur.fetchone()[0])


def upload_recording_to_database(conn, recording) -> None:
    """Inserts cleaned data into the database, creating any missing related records before inserting the final rows."""
    logger.info(f"Starting upload of {len(recording)} recording.")

    recording_to_insert = []

    with conn.cursor() as curs:
        for _, row in recording.iterrows():
            country_id = get_or_create_country_id(curs, row["origin_country"])

            botanist_id = get_or_create_botanist_id(
                curs,
                row["botanist_name"],
                row["email"],
                row["phone"],
            )

            plant_id = get_or_create_plant_id(
                curs,
                row["plant_name"],
                row["scientific_name"],
            )

            origin_location_id = get_or_create_origin_location_id(
                curs,
                row["origin_city"],
                country_id,
                row["longitude"],
                row["latitude"],
            )

            image_id = get_or_create_image_id(
                curs,
                row["license"],
                row["license_name"],
                row["license_url"],
                row["thumbnail"])

            recording_to_insert.append((
                plant_id,
                botanist_id,
                origin_location_id,
                row["last_watered"],
                image_id,
                row["recording_taken"],
                row["soil_moisture"],
                row["temperature"]
            ))

        query = """
        INSERT INTO beta.recording (
            plant_id, botanist_id, origin_location_id, last_watered,
            image_id, recording_taken, soil_moisture, temperature
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """

        curs.fast_executemany = True
        curs.executemany(query, recording_to_insert)

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
