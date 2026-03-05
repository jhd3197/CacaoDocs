"""Data models for the application."""


class User:
    """Represents a user in the system.

    Attributes:
        id (int): Unique identifier.
        name (str): Full name.
        email (str): Email address.
        is_active (bool): Whether the user account is active.
    """

    def __init__(self, name: str, email: str, is_active: bool = True):
        """Initialize a new User.

        Args:
            name (str): The user's full name.
            email (str): The user's email address.
            is_active (bool): Account status. Defaults to True.
        """
        self.name = name
        self.email = email
        self.is_active = is_active

    def deactivate(self):
        """Deactivate this user account.

        Returns:
            bool: True if successfully deactivated.

        Raises:
            ValueError: If user is already inactive.
        """
        if not self.is_active:
            raise ValueError("User is already inactive")
        self.is_active = False
        return True

    def to_dict(self) -> dict:
        """Convert user to dictionary representation.

        Returns:
            dict: User data as a dictionary.

        Examples:
            >>> user = User("Alice", "alice@example.com")
            >>> user.to_dict()
            {"name": "Alice", "email": "alice@example.com", "is_active": True}
        """
        return {
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
        }
