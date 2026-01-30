"""This script will have the base figures to be plotted and then displayed on the dashboard."""

from os import environ as ENV

from dotenv import load_dotenv
import pandas as pd
import altair as alt

from load_data import get_db_connection, load_data

load_dotenv()
df = load_data(get_db_connection(ENV))


def bar_chart(data, x_col, y_col, title):
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(f"{x_col}:Q", title=x_col.title() + " (ºC)" if x_col == 'temperature' else
                    x_col.replace("_", " ").title() + " (ml)"),
            y=alt.Y(f"{y_col}:N", sort="-x", title="Plant"),
            color=alt.value('palevioletred'),
            tooltip=[y_col, x_col]
        )
        .properties(title=title, height=250)
    )


def plot_temp_over_time(df):
    """Plots temperature over time for each plant."""
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("recording_taken:T", title="Time (hours)"),
        y=alt.Y("temperature:Q", title="Temperature (ºC)"),
        color=alt.value('orchid')
    ).properties(
        title="Temperature over Time"
    )
    return chart


def plot_moisture_over_time(df):
    """Plots soil moisture over time for each plant."""
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("recording_taken:T", title="Time (hours)"),
        y=alt.Y("soil_moisture:Q", title="Soil Moisture (ml)"),
        color=alt.value('orchid')
    ).properties(
        title="Soil Moisture over Time"
    )
    return chart
