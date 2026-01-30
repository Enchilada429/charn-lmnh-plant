"""This script contains helper functions to fetch the relevant data from the database to be plotted and displayed
on the dashboard."""

import logging
from os import _Environ

import pandas as pd
import streamlit as st
from pyodbc import connect, Connection
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()


@st.cache_resource
def get_db_connection(_config: _Environ) -> Connection:
    """Create and return a SQL Server connection."""
    conn_str = (
        f"DRIVER={{{_config['DB_DRIVER']}}};"
        f"SERVER={_config['DB_HOST']},{_config['DB_PORT']};"
        f"DATABASE={_config['DB_NAME']};"
        f"UID={_config['DB_USERNAME']};"
        f"PWD={_config['DB_PASSWORD']};"
        f"Encrypt=no;"
    )
    logging.info("Connecting to SQL Server.")
    conn = connect(conn_str)
    logging.info("Connection established.")

    return conn

def load_data(_conn: Connection, past_mins: int) -> pd.DataFrame:
    """This loads the cleaned plant recording data."""
    query = f"""
        SELECT r.plant_id, p.common_name, recording_taken, temperature, soil_moisture 
        FROM beta.recording r JOIN beta.plant p
        ON (r.plant_id=p.plant_id)
        WHERE recording_taken >= DATEADD(minute, {-1 * past_mins}, GETDATE())
        ORDER BY recording_taken;
        """
    df = pd.read_sql_query(query, _conn)
    return df
