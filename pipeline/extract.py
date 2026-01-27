"""Script for extracting data from the API."""

import pandas as pd
from requests import get


PLANT_ENDPOINT = "https://tools.sigmalabs.co.uk/api/plants/"


def get_api_plant_data(id: int) -> dict:
    """Returns the data as a dict on a single plant using its id."""

    return get(PLANT_ENDPOINT + id).json()


def extract_data_as_df() -> pd.DataFrame:
    """Extracts plant information from the API"""

    ...


if __name__ == "__main__":

    print(get_api_plant_data(1))
