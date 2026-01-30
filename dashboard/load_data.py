"""This script contains helper functions to fetch the relevant data from the database to be plotted and displayed
on the dashboard."""

from os import environ as ENV

import logging

import connectorx as cx
import pandas as pd
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()


def load_data(past_mins: int) -> pd.DataFrame:
    """This loads the cleaned plant recording data."""
    query = f"""
        SELECT r.plant_id, p.common_name, recording_taken, temperature, soil_moisture 
        FROM beta.recording r JOIN beta.plant p
        ON (r.plant_id=p.plant_id)
        WHERE recording_taken >= DATEADD(minute, {-1 * past_mins}, GETDATE())
        ORDER BY recording_taken;
        """

    conn_url = f"mssql://{ENV["DB_USERNAME"]}:{ENV["DB_PASSWORD"]}@{ENV["DB_HOST"]}:{ENV["DB_PORT"]}/{ENV["DB_NAME"]}"
    df = cx.read_sql(
        conn_url, query, partition_on="plant_id", partition_num=10)

    return df
