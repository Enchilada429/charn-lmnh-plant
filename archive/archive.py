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


def handler(event=None, context=None):
    bucket = os.environ["S3_BUCKET"]
    prefix = os.getenv("S3_PREFIX", "archive/")
    csv_path = "/tmp/past_data_archive.csv"

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    s3_key = f"{prefix}past_data_{date_str}.csv"

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

    conn_str = (
        f"DRIVER={{{os.environ['DB_DRIVER']}}};"
        f"SERVER={os.environ['DB_HOST']},{os.environ['DB_PORT']};"
        f"DATABASE={os.environ['DB_NAME']};"
        f"UID={os.environ['DB_USERNAME']};"
        f"PWD={os.environ['DB_PASSWORD']};"
        f"Encrypt=no;"
    )

    logging.info("Connecting to SQL server")
    conn = pyodbc.connect(conn_str)

    try:
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
        FROM dbo.recording
        WHERE recording_taken < DATEADD(hour, -24, GETUTCDATE());
        """

        logging.info("Selecting rows older than 24 hour")
        cur = conn.cursor()
        cur.execute(select_sql)

        row_count = 0
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)

            while True:
                rows = cur.fetchmany(10_000)
                if not rows:
                    break
                writer.writerows(rows)
                row_count += len(rows)

        cur.close()

        if row_count == 0:
            logging.info("No more rows")
            return {"archived_rows": 0}

        logging.info("Archived %d rows to CSV", row_count)

        logging.info("Uploading to s3://%s/%s", bucket, s3_key)
        boto3.client("s3").upload_file(csv_path, bucket, s3_key)
        logging.info("Upload complete")

        delete_sql = """
        DELETE FROM recording
        WHERE recording_taken < DATEADD(hour, -24, GETUTCDATE());
        """

        logging.info("Deleting archived rows from SQL server")
        conn.cursor().execute(delete_sql)
        conn.commit()
        logging.info("rRows have been deleted.")

        return {
            "Message": f"archived {row_count} rows",
            "s3_key": s3_key
        }

    finally:
        conn.close()
        logging.info("DB connection is closed")


if __name__ == "__main__":
    print(handler())
