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


def generate_country_id(conn: pyodbc.Connection, country_name: str) -> int:
    """Creates a new country row with given country name.
    Returns the id of the new country."""

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO beta.country (country_name) OUTPUT country_id VALUES (?);",
            (country_name,),
        )

        return int(cur.fetchone()[0])


def get_country_id(conn: pyodbc.Connection, country_name: str) -> int:
    """Returns the country id given a country name.
    Will make a new country in the database if invalid."""

    cached_id = get_id_from_cache("country_ids", country_name)

    if cached_id:
        return cached_id

    with conn.cursor() as cur:
        cur.execute(
            "SELECT country_id FROM beta.country WHERE country_name = ?;",
            (country_name,),
        )
        row = cur.fetchone()

    if row:
        id = int(row[0])
    else:
        id = generate_country_id(conn, country_name)
        add_id_to_cache("country_ids", country_name, id)

    return id


def generate_botanist_id(conn: pyodbc.Connection, name: str, email: str, phone: str) -> int:
    """Creates a new botanist row with given botanist details.
    Returns the id of the new botanist."""

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO beta.botanist (botanist_name, email, phone) OUTPUT botanist_id VALUES (?, ?, ?);",
            (name, email, phone),
        )

        return int(cur.fetchone()[0])


def get_botanist_id(conn: pyodbc.Connection, name: str, email: str, phone: str):
    """Returns the botanist id given the botanist details.
    Will make a new botanist in the database if invalid."""

    cached_id = get_id_from_cache("botanist_ids", email)

    if cached_id:
        return cached_id

    with conn.cursor() as cur:
        cur.execute(
            "SELECT botanist_id FROM beta.botanist WHERE email = ?;",
            (email,),
        )
        row = cur.fetchone()

    if row:
        id = int(row[0])
    else:
        id = generate_botanist_id(conn, name, email, phone)
        add_id_to_cache("botanist_ids", email, id)

    return id


def generate_plant_id(conn: pyodbc.Connection, common_name: str, scientific_name: str | None) -> int:
    """Creates a new plant row with given plant details.
    Returns the id of the new plant."""

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO beta.plant (common_name, scientific_name) OUTPUT plant_id VALUES (?, ?);",
            (common_name, scientific_name),
        )

        return int(cur.fetchone()[0])


def get_plant_id(conn: pyodbc.Connection, common_name: str, scientific_name: str | None) -> int:
    """Returns the plant id given the plant details.
    Will make a new plant in the database if invalid."""

    cached_id = get_id_from_cache("plant_ids", common_name)

    if cached_id:
        return cached_id

    with conn.cursor() as cur:
        cur.execute(
            "SELECT plant_id FROM beta.plant WHERE common_name = ?;",
            (common_name,),
        )
        row = cur.fetchone()

    if row:
        id = int(row[0])
    else:
        id = generate_plant_id(conn, common_name, scientific_name)
        add_id_to_cache("plant_ids", common_name, id)

    return id


def generate_image_id(conn: pyodbc.Connection, license: int, license_name: str, license_url: str, thumbnail: str | None) -> int:
    """Creates a new image row with given image details.
    Returns the id of the new image."""

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO beta.plant_image (licence, licence_name, licence_url, thumbnail) OUTPUT image_id VALUES (?, ?, ?, ?);",
            (license, license_name, license_url, thumbnail,),
        )

        return int(cur.fetchone()[0])


def get_image_id(conn: pyodbc.Connection, license: int, license_name: str, license_url: str, thumbnail: str | None) -> int:
    """Returns the image id given the image details.
    Will make a new image in the database if invalid."""

    cached_id = get_id_from_cache("image_ids", license)

    if cached_id:
        return cached_id

    with conn.cursor() as cur:
        cur.execute(
            "SELECT image_id FROM beta.plant_image WHERE licence = ?;",
            (license,),
        )
        row = cur.fetchone()

    if row:
        id = int(row[0])
    else:
        id = generate_image_id(
            conn, license, license_name, license_url, thumbnail)
        add_id_to_cache("image_ids", license, id)

    return id


def generate_origin_location_id(conn: pyodbc.Connection, city: str, country_id: int, longitude: float, latitude: float) -> int:
    """Creates a new origin location row with given origin location details.
    Returns the id of the new origin location."""

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO beta.origin_location (origin_city_name, country_id, longitude, latitude)
            OUTPUT origin_location_id
            VALUES (?, ?, ?, ?);
            """,
            (city, country_id, longitude, latitude),
        )

        return int(cur.fetchone()[0])


def get_origin_location_id(conn: pyodbc.Connection, city: str, country_id: int, longitude: float, latitude: float) -> int:
    """Returns the origin location id given the origin location details.
    Will make a new origin location in the database if invalid."""

    with conn.cursor() as cur:
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
        id = int(row[0])
    else:
        id = generate_origin_location_id(
            conn, city, country_id, longitude, latitude)

    return id


def upload_data_to_database(conn: pyodbc.Connection, data_df: DataFrame) -> None:
    """Inserts cleaned data into the database, creating any missing related records before inserting the final rows."""

    start_time = perf_counter()

    logger.info(f"Upload started for {len(data_df)} data points.")

    data_to_insert = []

    for _, row in data_df.iterrows():
        country_id = get_country_id(conn, row["origin_country"])

        botanist_id = get_botanist_id(
            conn,
            row["botanist_name"],
            row["email"],
            row["phone"],
        )

        plant_id = get_plant_id(
            conn,
            row["plant_name"],
            row["scientific_name"],
        )

        origin_location_id = get_origin_location_id(
            conn,
            row["origin_city"],
            country_id,
            row["longitude"],
            row["latitude"],
        )

        image_id = get_image_id(
            conn,
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

    with conn.cursor() as cur:
        cur.fast_executemany = True
        cur.executemany(query, data_to_insert)

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
