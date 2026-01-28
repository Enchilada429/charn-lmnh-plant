"""Script for executing the entire ETL pipeline."""

from os import environ as ENV

from logging import getLogger, INFO
from time import perf_counter
from dotenv import load_dotenv

from extract import extract
from transform import transform_data
from load import get_db_connection, upload_recording_to_database

logger = getLogger()
logger.setLevel(INFO)


def handler(event=None, context=None):
    """Executes the entire ETL pipeline. Is formatted as a Lambda function."""

    start_time = perf_counter()

    logger.info("ETL Pipeline started.")

    extracted_data = extract()
    cleaned_data = transform_data(extracted_data)

    conn = get_db_connection(ENV)
    upload_recording_to_database(conn, cleaned_data)

    conn.close()

    logger.info(
        f"ETL Pipeline finished in {perf_counter() - start_time} seconds.")


if __name__ == "__main__":

    load_dotenv()
