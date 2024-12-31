from typing import Dict, List, Optional
from datetime import datetime
from .user import User, Address
from .locations import City, Country

class MockDatabase:
    """Mock database for storing and retrieving user data."""
    
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1
        
        # Sample location data
        self._sample_locations = {
            'US': Country(
                id='1',
                code='US',
                name='United States',
                phone_code='+1',
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            'UK': Country(
                id='2',
                code='UK',
                name='United Kingdom',
                phone_code='+44',
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        }
        
        self._sample_cities = {
            'Boston': City(
                id='1',
                name='Boston',
                state='Massachusetts',
                country_code='US',
                latitude=42.3601,
                longitude=-71.0589,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            'London': City(
                id='2',
                name='London',
                state='England',
                country_code='UK',
                latitude=51.5074,
                longitude=-0.1278,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        }
        
        # Add some sample data
        self.add_sample_data()
    
    def add_sample_data(self):
        """Add sample users to the database."""
        sample_user = User(
            id=self._next_id,
            username="johndoe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            addresses=[
                Address(
                    street="123 Main St",
                    city=self._sample_cities['Boston'],
                    country=self._sample_locations['US'],
                    postal_code="02101"
                )
            ],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self._users[self._next_id] = sample_user
        self._next_id += 1

    def create_user(self, data: dict) -> User:
        """Create a new user.""" 
        user_id = self._next_id
        self._next_id += 1
        
        now = datetime.now()
        user_data = {
            'id': user_id,
            'created_at': now,
            'updated_at': now,
            **data
        }
        
        user = User.from_dict(user_data)
        self._users[user_id] = user
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID."""
        return self._users.get(user_id)

    def update_user(self, user_id: int, data: dict) -> Optional[User]:
        """Update a user's information."""
        if user := self._users.get(user_id):
            updated_data = user.to_dict()
            updated_data.update(data)
            updated_data['updated_at'] = datetime.now()
            
            updated_user = User.from_dict(updated_data)
            self._users[user_id] = updated_user
            return updated_user
        return None

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID."""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def list_users(self) -> List[User]:
        """List all users."""
        return list(self._users.values())
