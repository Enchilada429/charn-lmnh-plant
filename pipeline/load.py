"""Script for uploading the cleaned data to the RDS (SQL Server)."""

from time import perf_counter
from logging import getLogger, basicConfig, INFO
from os import environ as ENV, _Environ

import pyodbc
from dotenv import load_dotenv
from pandas import DataFrame

from extract import extract
from transform import transform_data


logger = getLogger(__name__)

ID_CACHE = {
    "country_ids": {},
    "botanist_ids": {},
    "plant_ids": {},
    "image_ids": {}
}


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


def get_id_from_cache(id_collection_name: str, id_info: str) -> int:
    """Returns an ID if it exists in the ID cache. 
    If not found, adds to ID cache and returns None."""

    id_collection = ID_CACHE.get(id_collection_name)

    if not id_collection:
        return None

    return id_collection.get(id_info)


def add_id_to_cache(id_collection_name: str, id_info: str, id: int) -> None:
    """Adds an ID to the ID cache. If the collection name is not found, does not add."""

    id_collection = ID_CACHE.get(id_collection_name)

    if id_collection:
        ID_CACHE[id_collection_name][id_info] = id


def get_or_create_country_id(cur: pyodbc.Cursor, country_name: str) -> int:
    """Gets or creates country_id"""

    cached_id = get_id_from_cache("country_ids", country_name)

    if cached_id:
        return cached_id

    cur.execute(
        "SELECT country_id FROM beta.country WHERE country_name = ?;",
        (country_name,),
    )
    row = cur.fetchone()
    if row:
        id = int(row[0])
        add_id_to_cache("country_ids", country_name, id)
        return id

    cur.execute(
        "INSERT INTO beta.country (country_name) OUTPUT country_id VALUES (?);",
        (country_name,),
    )

    id = int(cur.fetchone()[0])

    add_id_to_cache("country_ids", country_name, id)

    return


def get_or_create_botanist_id(cur: pyodbc.Cursor, name: str, email: str, phone: str):
    """Gets or creates botanist_id"""

    cached_id = get_id_from_cache("botanist_ids", email)

    if cached_id:
        return cached_id

    cur.execute(
        "SELECT botanist_id FROM beta.botanist WHERE email = ?;",
        (email,),
    )
    row = cur.fetchone()
    if row:
        id = int(row[0])
        add_id_to_cache("botanist_ids", email, id)
        return id

    cur.execute(
        "INSERT INTO beta.botanist (botanist_name, email, phone) OUTPUT botanist_id VALUES (?, ?, ?);",
        (name, email, phone),
    )

    id = int(cur.fetchone()[0])

    add_id_to_cache("botanist_ids", email, id)

    return


def get_or_create_plant_id(cur: pyodbc.Cursor, common_name: str, scientific_name: str | None) -> int:
    """Gets or creates plant_id"""

    cached_id = get_id_from_cache("plant_ids", common_name)

    if cached_id:
        return cached_id

    cur.execute(
        "SELECT plant_id FROM beta.plant WHERE common_name = ?;",
        (common_name,),
    )
    row = cur.fetchone()
    if row:
        id = int(row[0])
        add_id_to_cache("plant_ids", common_name, id)
        return id

    cur.execute(
        "INSERT INTO beta.plant (common_name, scientific_name) OUTPUT plant_id VALUES (?, ?);",
        (common_name, scientific_name),
    )

    id = int(cur.fetchone()[0])

    add_id_to_cache("plant_ids", common_name, id)

    return


def get_or_create_image_id(cur: pyodbc.Cursor, license: int, license_name: str, license_url: str, thumbnail: str | None) -> int:
    """Gets or creates image_id"""

    cached_id = get_id_from_cache("image_ids", license)

    if cached_id:
        return cached_id

    cur.execute(
        "SELECT image_id FROM beta.plant_image WHERE licence = ?;",
        (license,),
    )
    row = cur.fetchone()
    if row:
        id = int(row[0])
        add_id_to_cache("image_ids", license, id)
        return id

    cur.execute(
        "INSERT INTO beta.plant_image (licence, licence_name, licence_url, thumbnail) OUTPUT image_id VALUES (?, ?, ?, ?);",
        (license, license_name, license_url, thumbnail,),
    )

    id = int(cur.fetchone()[0])

    add_id_to_cache("image_ids", license, id)

    return


def get_or_create_origin_location_id(cur: pyodbc.Cursor, city: str, country_id: int, longitude, latitude) -> int:
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
        OUTPUT origin_location_id
        VALUES (?, ?, ?, ?);
        """,
        (city, country_id, longitude, latitude),
    )

    return int(cur.fetchone()[0])


def upload_data_to_database(conn: pyodbc.Connection, data_df: DataFrame) -> None:
    """Inserts cleaned data into the database, creating any missing related records before inserting the final rows."""

    start_time = perf_counter()

    logger.info(f"Upload started for {len(data_df)} entries.")

    data_to_insert = []

    with conn.cursor() as curs:
        for _, row in data_df.iterrows():
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

            data_to_insert.append((
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
        curs.executemany(query, data_to_insert)

    conn.commit()

    logger.info(
        f"Upload finished of {len(data_to_insert)} data points with time taken: {perf_counter() - start_time} seconds.")


if __name__ == "__main__":

    basicConfig(level=INFO)

    load_dotenv()

    extracted_data = extract()
    df_transformed = transform_data(extracted_data)

    conn = get_db_connection(ENV)
    try:
        upload_data_to_database(conn, df_transformed)
    finally:
        conn.close()
