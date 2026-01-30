"""Script which creates classes for plant information."""

from datetime import datetime


class Plants:
    """Class for a collection of plants."""

    def __init__(self, plants: list[Plant] = []):
        """Initialises the collection of plants."""
        self.plants = plants

    def get_plant(self, common_name: str) -> Plant:
        """Returns a plant based on its common name. Returns None if not found."""

        for plant in self.plants:
            if plant.common_name == common_name:
                return plant

        return None

    def add_plant(self, plant: Plant) -> None:
        """Adds a plant to the collection of plants."""

        self.plants.append(plant)

    def remove_plant(self, plant: Plant) -> None:
        """Removes a plant from the collection of plants."""

        self.plants = [p for p in self.plants if p == plant]


class Plant:
    """Class for a single plant."""

    def __init__(self,
                 common_name: str,
                 botanist: Botanist = None,
                 origin: Origin = None,
                 image: Image = None,
                 scientific_name: str = None,
                 soil_moisture: float = None,
                 temperature: float = None,
                 last_watered: datetime = None,
                 recording_taken: datetime = None):
        """Initialises plant information."""

        self.common_name = common_name
        self.botanist = botanist
        self.origin = origin

        self.image = image
        self.scientific_name = scientific_name
        self.soil_moisture = soil_moisture
        self.temperature = temperature
        self.last_watered = last_watered
        self.recording_taken = recording_taken


class Botanist:
    """Class for a single botanist."""

    def __init__(self, name: str, email: str, phone: str):
        """Initialises the botanist's info."""
        self.name = name
        self.email = email
        self.phone = phone


class Origin:
    """Class for an origin, where a plant comes from."""

    def __init__(self, city: str, country: str, longitude: float, latitude: float):
        """Initialises the information on the origin location."""
        self.city = city
        self.country = country
        self.longitude = longitude
        self.latitude = latitude


class Image:
    """Class for info of an image of a plant."""

    def __init__(self, licence: int, licence_name: str, licence_url: str, thumbnail: str):
        """Initialises the image info."""
        self.licence = licence
        self.licence_name = licence_name
        self.licence_url = licence_url
        self.thumbnail = thumbnail
