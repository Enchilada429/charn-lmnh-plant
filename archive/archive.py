"""Script that selects data that is older than 24 hours, saves it as a .CSV, uploads it to an S3 bucket, then deletes it from the DB"""
import os
import csv
import logging
from datetime import datetime, timezone

import boto3
import pyodbc


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def get_s3_details():
    """Retrieves S3 details from .ENV"""
    bucket = os.environ["S3_BUCKET"]
    prefix = os.getenv("S3_PREFIX", "archive/")
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    s3_key = f"{prefix}past_data_{date_str}.csv"
    return bucket, s3_key


def get_db_connection():
    """Connects to the DB using credentials in .ENV"""
    conn_str = (
        f"DRIVER={{{os.environ['DB_DRIVER']}}};"
        f"SERVER={os.environ['DB_HOST']},{os.environ['DB_PORT']};"
        f"DATABASE={os.environ['DB_NAME']};"
        f"UID={os.environ['DB_USERNAME']};"
        f"PWD={os.environ['DB_PASSWORD']};"
        f"Encrypt=no;"
    )

    logging.info("Connecting to SQL server")
    return pyodbc.connect(conn_str)


def write_old_data_to_csv(conn, csv_path, columns):
    """Produces CSV file containing selected rows"""
    select_sql = """
    SELECT
        plant_id,
        botanist_id,
        origin_location_id,
        last_watered,
        image_id,
        recording_taken,
        soil_moisture,
        temperature
    FROM beta.recording
    WHERE recording_taken < DATEADD(hour, -24, GETUTCDATE());
    """

    logging.info("Selecting rows older than 24 hour")
    cur = conn.cursor()
    cur.execute(select_sql)

    row_count = 0
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)

        rows = cur.fetchmany(10_000)
        while rows:
            writer.writerows(rows)
            row_count += len(rows)
            rows = cur.fetchmany(10_000)

    cur.close()
    return row_count


def upload_csv_to_s3(csv_path, bucket, s3_key):
    """Upload created CSV files to the S3 bucket"""
    logging.info("Uploading to s3://%s/%s", bucket, s3_key)
    boto3.client("s3").upload_file(csv_path, bucket, s3_key)
    logging.info("Upload complete")


def delete_old_data(conn):
    """Deletes the selected data from the DB"""
    delete_sql = """
    DELETE FROM recording
    WHERE recording_taken < DATEADD(hour, -24, GETUTCDATE());
    """

    logging.info("Deleting archived rows from SQL server")
    conn.cursor().execute(delete_sql)
    conn.commit()
    logging.info("Rows have been deleted.")


def handler(event=None, context=None):
    """Archives database data older than 24 hours to S3 and removes them from the database."""
    csv_path = "/tmp/past_data_archive.csv"

    columns = [
        "plant_id",
        "botanist_id",
        "origin_location_id",
        "last_watered",
        "image_id",
        "recording_taken",
        "soil_moisture",
        "temperature",
    ]

    bucket, s3_key = get_s3_details()
    conn = get_db_connection()

    try:
        row_count = write_old_data_to_csv(conn, csv_path, columns)

        if row_count == 0:
            logging.info("No more rows")
            return {"archived_rows": 0}

        logging.info("Archived %d rows to CSV", row_count)

        upload_csv_to_s3(csv_path, bucket, s3_key)
        delete_old_data(conn)

        return {
            "Message": f"archived {row_count} rows",
            "s3_key": s3_key
        }

    finally:
        conn.close()
        logging.info("DB connection is closed")


if __name__ == "__main__":
    print(handler())
