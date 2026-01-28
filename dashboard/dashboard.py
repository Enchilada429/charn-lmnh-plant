"""Script for hosting the dashboard for the past 24 hours of data."""

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from dotenv import load_dotenv
from load_data import load_data
from charts import bar_chart

if __name__ == '__main__':
    load_dotenv()
    
    plant_recordings = load_data()

    top_5_temp = df.nlargest(5, "temperature")
    bottom_5_temp = df.nsmallest(5, "temperature")
    top_5_moist = df.nlargest(5, "soil_moisture")
    bottom_5_moist = df.nsmallest(5, "soil_moisture")


    st_autorefresh(interval=5000, key='refresh')

    st.set_page_config(
        page_title="LMNH Plant Monitor",
        layout="wide"
    )

    st.title(" 🌱 LMNH Plant Monitoring Dashboard ")

    st.subheader(" Alerts 🥀")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Temperature Extremes")
        st.altair_chart(
            bar_chart(top_5_temp, "temperature", "plant_name", "Top 5 Highest Temperatures"),
            use_container_width=True,
        )

        st.altair_chart(
            bar_chart(bottom_5_temp, "temperature", "plant_name", "Top 5 Lowest Temperatures"),
            use_container_width=True,
        )

    with col2:
        st.subheader("Soil Moisture Extremes")
        st.altair_chart(
            bar_chart(top_5_moist, "soil_moisture", "plant_name", "Top 5 Highest Soil Moisture"),
            use_container_width=True,
        )

        st.altair_chart(
            bar_chart(bottom_5_moist, "soil_moisture", "plant_name", "Top 5 Lowest Soil Moisture"),
            use_container_width=True,
        )


    st.sidebar.header("🌿 Plant Selection")
    plant = st.sidebar.selectbox(
        "Select a plant",
        sorted(df["plant_name"].dropna().unique())
    )
    plant_df = df[df["plant_name"] == plant].sort_values("recording_taken")