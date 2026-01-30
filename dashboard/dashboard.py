"""Script for hosting the dashboard for the past 24 hours of data."""

from os import environ as ENV
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from dotenv import load_dotenv

from load_data import get_db_connection, load_data
from charts import bar_chart, plot_temp_over_time, plot_moisture_over_time
from classes import Plants, Plant, Botanist, Origin, Image


def get_latest_recording_for_plant(plant_recordings: pd.DataFrame, plant_name: str) -> dict:
    """Returns a dict for the latest recording for the plant."""

    plant_df = plant_recordings[plant_recordings["common_name"] == plant_name]
    plant_df = plant_df.sort_values(
        by=["recording_taken"], ascending=False)

    latest_row = plant_df.head(1)

    return {
        "common_name": latest_row.iloc[0]["common_name"],
        "soil_moisture": latest_row.iloc[0]["soil_moisture"],
        "temperature": latest_row.iloc[0]["temperature"],
        "recording_taken": latest_row.iloc[0]["recording_taken"]
    }


def get_plant_collection(plant_recordings: pd.DataFrame) -> Plants:
    """Returns a Plants object which is a collection of plants
    based on the plants information extracted from the data."""

    plant_collection = Plants()

    for plant_name in plant_recordings["common_name"].dropna().unique():
        latest_recording = get_latest_recording_for_plant(
            plant_recordings, plant_name)

        plant_collection.add_plant(
            Plant(
                common_name=latest_recording["common_name"],
                soil_moisture=latest_recording["soil_moisture"],
                temperature=latest_recording["temperature"],
                recording_taken=latest_recording["recording_taken"]
            )
        )

    return plant_collection


def update_plant_collection(plant_collection: Plants, plant_recordings: pd.DataFrame) -> None:
    """Updates fields in the plant collection based on new data."""

    for plant in plant_collection.plants:
        latest_recording = get_latest_recording_for_plant(
            plant_recordings, plant.common_name)

        plant.soil_moisture = latest_recording["soil_moisture"]
        plant.temperature = latest_recording["temperature"]
        plant.recording_taken = latest_recording["recording_taken"]


def display_dashboard(plant_recordings: pd.DataFrame, plant_collection: Plants):
    """Outputs the main visualisations of the dashboard."""

    top_5_temp = plant_recordings.nlargest(5, "temperature")
    bottom_5_temp = plant_recordings.nsmallest(5, "temperature")
    top_5_moist = plant_recordings.nlargest(5, "soil_moisture")
    bottom_5_moist = plant_recordings.nsmallest(5, "soil_moisture")

    st.set_page_config(
        page_title="LMNH Plant Monitor",
        layout="wide"
    )

    st.title(" 🌱 LMNH Plant Monitoring Dashboard ")
    st.divider()
    st.subheader(" Alerts 🥀")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Temperature Extremes")
        st.altair_chart(
            bar_chart(top_5_temp, "temperature",
                      "common_name", "Highest Temperatures")
        )

        st.altair_chart(
            bar_chart(bottom_5_temp, "temperature",
                      "common_name", "Lowest Temperatures")
        )

    with col2:
        st.subheader("Soil Moisture Extremes")
        st.altair_chart(
            bar_chart(top_5_moist, "soil_moisture",
                      "common_name", "Highest Soil Moisture")
        )

        st.altair_chart(
            bar_chart(bottom_5_moist, "soil_moisture",
                      "common_name", "Lowest Soil Moisture")
        )
    st.divider()

    st.sidebar.header("🌿 Plant Selection")
    plant = st.sidebar.selectbox(
        "Select a plant",
        sorted(plant_recordings["common_name"].dropna().unique())
    )
    plant_df = plant_recordings[plant_recordings["common_name"] == plant].sort_values(
        "recording_taken")

    st.subheader(f"📈 {plant} – Last 24 Hours")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(
            plot_temp_over_time(plant_df)
        )

        plant_obj = plant_collection.get_plant(plant)

        st.info(f"Current temperature: {plant_obj.temperature:.2f} ºC")
        st.info(f"Recording taken: {plant_obj.recording_taken}")
        st.info(f"Last watered: {plant_obj.recording_taken}")

    with col2:
        st.altair_chart(
            plot_moisture_over_time(plant_df)
        )

        st.info(f"Current soil moisture: {plant_obj.soil_moisture:.2f} ml")


if __name__ == '__main__':

    if "initialised" not in st.session_state:
        st.session_state.initialised = True
        load_dotenv()

        st.session_state.conn = get_db_connection(ENV)
        st.session_state.df = load_data(st.session_state.conn, 1440)
        st.session_state.plant_collection = get_plant_collection(
            st.session_state.df)

    st_autorefresh(interval=60000, key='refresh')

    display_dashboard(st.session_state.df, st.session_state.plant_collection)

    st.session_state.df = pd.concat(
        [st.session_state.df, load_data(st.session_state.conn, 1)])

    st.session_state.df = st.session_state.df[st.session_state.df["recording_taken"] > datetime.now(
    ) - timedelta(hours=1)]

    update_plant_collection(
        st.session_state.plant_collection, st.session_state.df)
