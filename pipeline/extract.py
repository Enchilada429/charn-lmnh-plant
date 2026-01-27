"""Script for extracting data from the API."""

from requests import get
from logging import getLogger, INFO

import aiohttp
import asyncio

logger = getLogger(__name__)

PLANT_ENDPOINT = "https://tools.sigmalabs.co.uk/api/plants/"


async def get_plant_data(session: aiohttp.ClientSession, id: int) -> dict:
    """Returns the data as a dict on a single plant using its id via the API."""

    async with session.get(PLANT_ENDPOINT + str(id)) as response:
        data = await response.json()
        return data


async def get_all_plants_data() -> list[dict]:
    """Returns the data on all plants via the API.
    Only stops when meeting 20 consecutive errors in data in a row."""

    logger.info("Retrieving data on all plants.")

    async with aiohttp.ClientSession() as session:
        tasks = [get_plant_data(session, id) for id in range(50)]
        results = await asyncio.gather(*tasks)

    logger.info("Finished retrieving data on all plants.")

    return results


if __name__ == "__main__":

    logger.setLevel(INFO)

    print(asyncio.run(get_all_plants_data()))
