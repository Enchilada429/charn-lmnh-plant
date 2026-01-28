"""This script contains helper functions to fetch the relevant data from the database to be plotted and displayed
on the dashboard."""

import logging
from os import environ as ENV

import pandas as pd
import streamlit as st
from pyodbc import connect, Connection
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

@st.cache_resource
def get_db_connection() -> Connection:
    """Connects to the DB."""
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USERNAME']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")
    return connect(conn_str)


@st.cache_data
def load_data(csv_path, data_source: str='db') -> pd.DataFrame:
    """This loads the cleaned plant recording data. This is a static version of the RDS data that will be used."""
    
    if not data_source:
        logging.warning("No data soure.")
    
    if data_source == 'csv':
        if not csv_path:
            raise ValueError("csv_path must be provided when source='csv'")
        df = pd.read_csv(csv_path)
        df["recording_taken"] = pd.to_datetime(df["recording_taken"])
        return df

    if data_source == 'db':
        conn = get_db_connection()
        query = """
        SELECT plant_id,
                common_name,
                recording_taken,
                temperature,
                soil_moisture,
        FROM recording
        ORDER BY recording_taken
        """
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchone()
        conn.close()
        return [list(row) for row in data]
