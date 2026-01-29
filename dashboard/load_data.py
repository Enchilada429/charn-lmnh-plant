"""This script contains helper functions to fetch the relevant data from the database to be plotted and displayed
on the dashboard."""

import logging
from os import environ as ENV
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


@st.cache_data
def load_data() -> pd.DataFrame:
    """This loads the cleaned plant recording data. This is a static version of the RDS data that will be used."""
    conn = get_db_connection(ENV)
    query = """
        SELECT r.plant_id, p.common_name, recording_taken, temperature, soil_moisture 
        FROM beta.recording r JOIN beta.plant p
        ON (r.plant_id=p.plant_id)
        ORDER BY recording_taken;
        """
    df = pd.read_sql_query(query, conn)
    return df
