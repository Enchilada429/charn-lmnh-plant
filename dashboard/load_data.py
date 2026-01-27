"""This script contains helper functions to fetch the relevant data from the database to be plotted and displayed
on the dashboard."""

from os import environ as ENV

from dotenv import load_dotenv
from pyodbc import connect

def get_db_connection():
    """Connects to the DB."""
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USERNAME']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    return connect(conn_str)


def load_plant_over_time(conn, plant_id):
    """Fetches the temperature and moisture data for a single plant."""
    query = """
    SELECT recording_taken,
            temperature,
            soil_moisture
    FROM recording
    WHERE plant_id = ?
    ORDER BY recording_taken
    """
    with conn.cursor() as cur:
        cur.execute(query, (plant_id,))
        data = cur.fetchone()
    conn.close()
    return [list(row) for row in data]


if __name__ == '__main__':
    load_dotenv()