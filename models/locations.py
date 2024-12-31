from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from cacaodocs import CacaoDocs

@dataclass
@CacaoDocs.doc_api(doc_type="types", tag="locations")
class Country:
    """
    Description:
        Represents a country in the system.

    Args:
        id (str): Unique identifier for the country
        code (str): The ISO country code (e.g., 'US', 'UK')
        name (str): The full country name
        phone_code (str): International dialing code
        created_at (datetime): Timestamp when the record was created
        updated_at (datetime): Timestamp when the record was last updated
    """
    id: str
    code: str
    name: str
    phone_code: str
    created_at: datetime
    updated_at: datetime

@dataclass
@CacaoDocs.doc_api(doc_type="types", tag="locations")
class City:
    """
    Description:
        Represents a city within a country.

    Args:
        id (str): Unique identifier for the city
        name (str): The city name
        state (str): State or province name
        country_code (str): The ISO country code
        latitude (float): Geographic latitude
        longitude (float): Geographic longitude
        created_at (datetime): Timestamp when the record was created
        updated_at (datetime): Timestamp when the record was last updated
    """
    id: str
    name: str
    state: str
    country_code: str
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime
