"""Script for extracting data from the API."""

from requests import get
from logging import getLogger, INFO

logger = getLogger(__name__)

PLANT_ENDPOINT = "https://tools.sigmalabs.co.uk/api/plants/"


def get_api_plant_data(id: int) -> dict:
    """Returns the data as a dict on a single plant using its id via the API."""

    return get(PLANT_ENDPOINT + str(id)).json()


def get_all_plants_data() -> list[dict]:
    """Returns the data on all plants via the API.
    Only stops when meeting 5 consecutive errors in data in a row."""

    logger.info("Retrieving data on all plants.")

    id = 1
    consecutive_errors = 0
    error_limit = 5
    plants_data = []

    while consecutive_errors <= error_limit:
        plant_data = get_api_plant_data(id)
        is_error = plant_data.get("error")

        if is_error:
            consecutive_errors += 1
        else:
            plants_data.append(plant_data)
            consecutive_errors = 0

        id += 1

    logger.info("Finished retrieving data on all plants.")

    return plants_data


if __name__ == "__main__":

    logger.setLevel(INFO)

    print(get_all_plants_data())
