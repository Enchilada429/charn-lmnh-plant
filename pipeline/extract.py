"""Script for extracting data from the API."""

from time import perf_counter
from logging import getLogger, basicConfig, INFO

import aiohttp
import asyncio

logger = getLogger(__name__)

PLANT_ENDPOINT = "https://tools.sigmalabs.co.uk/api/plants/"


async def get_plant_data(session: aiohttp.ClientSession, plant_id: int) -> dict:
    """Returns a single plant's data using its id. Requires a session object."""

    async with session.get(PLANT_ENDPOINT + str(plant_id)) as response:
        data = await response.json()
        return data


async def get_all_plants_data(batch_processing_size: int) -> list[dict]:
    """Returns the data on all plants via the API.
    Only stops when meeting consecutive errors dictated by batch processing size argument."""

    plants_data = []
    plants_left = True
    id_counter = 1

    logger.info("Retrieving all plants data.")

    async with aiohttp.ClientSession() as session:
        while plants_left:
            tasks = [get_plant_data(session, plant_id)
                     for plant_id in range(id_counter, id_counter + batch_processing_size)]

            results = await asyncio.gather(*tasks)

            errorless_results = [
                result for result in results if "error" not in result.keys()]

            if len(errorless_results) == 0:
                plants_left = False
            else:
                plants_data.extend(errorless_results)
                id_counter += batch_processing_size

    logger.info("Retrieved all plants data.")

    return plants_data


def extract() -> list[dict]:
    """Extracts all data from the API and returns it. Takes care of async requests."""

    basicConfig(level=INFO)

    logger.info("Extraction started.")

    start_time = perf_counter()

    data = asyncio.run(get_all_plants_data(batch_processing_size=20))

    logger.info(
        f"Extraction finished with time taken: {perf_counter() - start_time} seconds.")

    return data


if __name__ == "__main__":
    extract()
