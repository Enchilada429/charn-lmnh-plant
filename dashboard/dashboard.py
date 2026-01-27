"""Script for hosting the dashboard for the past 24 hours of data."""

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd

from charts import plot_temp_over_time, plot_moisture_over_time

st_autorefresh(interval=5000, key='refresh')

st.set_page_config(
    page_title="LMNH Plant Monitor",
    layout="wide"
)

st.title(" 🌱 LMNH Plant Monitoring Dashboard ")

st.subheader(" Alerts 🥀")



st.sidebar.header("Controls")
st.sidebar.header("Data Archive")

# plant_name = st.sidebar.selectbox(
#     "Select Plant",
#     df['name']
# )

# plant_id = df.loc[
#     df['name'] == plant_name,
#     'plant_id'
# ].values[0]
