"""Script for hosting the dashboard for the past 24 hours of data."""

import streamlit as st
import pandas as pd

from charts import plot_temp_over_time, plot_moisture_over_time

st.title(" 🌱 LMNH Plant Monitoring Dashboard ")

