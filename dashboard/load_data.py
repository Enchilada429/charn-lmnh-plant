"""This script contains helper functions to fetch the relevant data from the database to be plotted and displayed
on the dashboard."""


def load_plants_over_time(conn, plant_id):
    """Fetches the temperature and moisture data for a single plant."""
    query = """
    SELECT recording_taken,
            temperature,
            soil_moisture
    FROM recording
    WHERE plant_id = ?
    ORDER BY recording_taken
    """
    return