"""Script for hosting the dashboard for the past 24 hours of data."""

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from dotenv import load_dotenv

from load_data import load_data
from charts import bar_chart, plot_temp_over_time, plot_moisture_over_time

def display_dashboard():
    """Outputs the main visualisations of the dashboard."""
    load_dotenv()
    plant_recordings = load_data()

    top_5_temp = plant_recordings.nlargest(5, "temperature")
    bottom_5_temp = plant_recordings.nsmallest(5, "temperature")
    top_5_moist = plant_recordings.nlargest(5, "soil_moisture")
    bottom_5_moist = plant_recordings.nsmallest(5, "soil_moisture")

    st_autorefresh(interval=5000, key='refresh')

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
            bar_chart(top_5_temp, "temperature", "common_name", "Highest Temperatures")
        )

        st.altair_chart(
            bar_chart(bottom_5_temp, "temperature", "common_name", "Lowest Temperatures")
        )

    with col2:
        st.subheader("Soil Moisture Extremes")
        st.altair_chart(
            bar_chart(top_5_moist, "soil_moisture", "common_name", "Highest Soil Moisture")
        )

        st.altair_chart(
            bar_chart(bottom_5_moist, "soil_moisture", "common_name", "Lowest Soil Moisture")
        )
    st.divider()

    st.sidebar.header("🌿 Plant Selection")
    plant = st.sidebar.selectbox(
        "Select a plant",
        sorted(plant_recordings["common_name"].dropna().unique())
    )
    plant_df = plant_recordings[plant_recordings["common_name"] == plant].sort_values("recording_taken")
    
    st.subheader(f"📈 {plant} – Last 24 Hours")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(
            plot_temp_over_time(plant_df)
        )

    with col2:
        st.altair_chart(
            plot_moisture_over_time(plant_df)
        )

if __name__ == '__main__':
    load_dotenv()
    display_dashboard()