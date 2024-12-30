from dataclasses import dataclass
from typing import Optional
from cacaodocs import CacaoDocs

@dataclass
@CacaoDocs.doc_api(doc_type="types", tag="locations")
class Country:
    """
    Description:
        Represents a country in the system.

    Args:
        code (str): The ISO country code (e.g., 'US', 'UK')
        name (str): The full country name
        phone_code (str): International dialing code
    """
    code: str
    name: str
    phone_code: str

@dataclass
@CacaoDocs.doc_api(doc_type="types", tag="locations")
class City:
    """
    Description:
        Represents a city within a country.

    Args:
        name (str): The city name
        state (str): State or province name
        country_code (str): The ISO country code
        latitude (float): Geographic latitude
        longitude (float): Geographic longitude
    """
    name: str
    state: str
    country_code: str
    latitude: float
    longitude: float
