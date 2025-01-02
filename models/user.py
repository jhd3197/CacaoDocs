from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List
from flask import json
from .locations import City, Country
from cacaodocs import CacaoDocs

@dataclass
@CacaoDocs.doc_api(doc_type="types", tag="locations")
class Address:
    """
    Description:
        Represents a user's address in the system.

    Args:
        street (str): Street name and number
        city (City): City information
        country (Country): Country information
        postal_code (str): Postal or ZIP code
    """
    street: str
    city: City
    country: Country
    postal_code: str

    def to_dict(self) -> dict:
        """Convert address to dictionary format."""
        return {
            'street': self.street,
            'city': asdict(self.city),
            'country': asdict(self.country),
            'postal_code': self.postal_code
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Address':
        """Create an Address instance from a dictionary."""
        return cls(
            street=data['street'],
            city=City(**data['city']),
            country=Country(**data['country']),
            postal_code=data['postal_code']
        )

@dataclass
@CacaoDocs.doc_api(doc_type="types", tag="models")
class User:
    """
    Description:
        Represents a user in the system with extended information.

    Args:
        id (int): The unique identifier
        username (str): The user's username
        email (str): The user's email address
        first_name (str): User's first name
        last_name (str): User's last name
        addresses (List[Address]): List of user's addresses
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last update timestamp
    """
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    addresses: List[Address]
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict:
        """Convert the user instance to a dictionary."""
        data = asdict(self)
        # Convert datetime objects to ISO format strings
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create a User instance from a dictionary."""
        # Convert ISO format strings to datetime objects
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if isinstance(data.get('updated_at'), str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        # Convert address dictionaries to Address objects
        if 'addresses' in data:
            data['addresses'] = [Address(**addr) for addr in data['addresses']]
            
        return cls(**data)

    def __json__(self):
        """Flask JSON serialization support."""
        return self.to_dict()
