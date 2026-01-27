"""Script for extracting data from the API."""

import aiohttp
import asyncio

from time import time

PLANT_ENDPOINT = "https://tools.sigmalabs.co.uk/api/plants/"


async def get_plant_data(session: aiohttp.ClientSession, id: int) -> dict:
    """Returns the data as a dict on a single plant using its id via the API."""

    async with session.get(PLANT_ENDPOINT + str(id)) as response:
        data = await response.json()
        return data


async def get_all_plants_data(batch_processing_size: int) -> list[dict]:
    """Returns the data on all plants via the API.
    Only stops when meeting consecutive errors dictated by batch processing size argument."""

    plants_data = []
    plants_left = True
    id_counter = 1

    async with aiohttp.ClientSession() as session:
        while plants_left:
            tasks = [get_plant_data(session, id)
                     for id in range(id_counter, id_counter + batch_processing_size)]

            results = await asyncio.gather(*tasks)

            errorless_results = [
                result for result in results if "error" not in result.keys()]

            if len(errorless_results) == 0:
                plants_left = False
            else:
                plants_data.extend(errorless_results)
                id_counter += batch_processing_size

    return plants_data


def extract() -> list[dict]:
    """Extracts all data from the API. Takes care of async requests."""

    start_time = time()

    data = asyncio.run(get_all_plants_data(batch_processing_size=20))

    print(f"Total extraction time: {time() - start_time} seconds")

    return data


if __name__ == "__main__":
    extract()
