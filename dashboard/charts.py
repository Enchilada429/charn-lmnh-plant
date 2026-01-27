"""This script will have the base figures to be plotted and then displayed on the dashboard."""

import pandas as pd
import altair as alt

from load_data import load_plant_over_time

def highest_temperatures(conn, df):
    """Plots a bar chart of the five highest temperatures in plants."""
    chart = alt.Chart(df).mark_bar(point=True).encode(
        x=alt.X("common_name:T", title="Plant"),
        y=alt.Y("temperature:Q", title="Temperature")
    ).properties(
        title="Highest Temperatures"
    )
    return chart


def highest_temperatures(conn, df):
    """Plots a bar chart of the five lowest temperatures in plants."""
    chart = alt.Chart(df).mark_bar(point=True).encode(
        x=alt.X("common_name:T", title="Plant"),
        y=alt.Y("temperature:Q", title="Temperature")
    ).properties(
        title="Lowest Temperatures"
    )
    return chart


def highest_moisture(conn, df):
    """Plots a bar chart of the five highest moistures in plants."""
    chart = alt.Chart(df).mark_bar(point=True).encode(
        x=alt.X("common_name:T", title="Plant"),
        y=alt.Y("soil_moisture:Q", title="Soil Moisture")
    ).properties(
        title="Highest Soil Moisture"
    )
    return chart


def lowest_moisture(conn, df):
    """Plots a bar chart of the five highest moistures in plants."""
    chart = alt.Chart(df).mark_bar(point=True).encode(
        x=alt.X("common_name:T", title="Plant"),
        y=alt.Y("soil_moisture:Q", title="Soil Moisture")
    ).properties(
        title="Lowest Soil Moisture"
    )
    return chart


def plot_temp_over_time(conn, df):
    """Plots temperature over time for each plant."""
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("recording_taken:T", title="Time"),
        y=alt.Y("temperature:Q", title="Temperature")
    ).properties(
        title="Temperature over Time"
    )
    return chart


def plot_moisture_over_time(conn, df):
    """Plots soil moisture over time for each plant."""
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("recording_taken:T", title="Time"),
        y=alt.Y("soil_moisture:Q", title="Soil Moisture")
    ).properties(
        title="Soil Moisture over Time"
    )
    return chart
