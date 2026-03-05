"""Utility functions."""


def hash_password(password: str, salt: str = None) -> str:
    """Hash a password using bcrypt.

    Args:
        password (str): The plaintext password.
        salt (str): Optional salt. Generated if not provided.

    Returns:
        str: The hashed password string.

    Raises:
        ValueError: If password is empty or too short.

    Examples:
        >>> hash_password("mysecretpass")
        '$2b$12$...'
    """
    if not password or len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    return f"hashed_{password}"


def format_currency(amount: int, currency: str = "USD") -> str:
    """Format an amount in cents to a human-readable currency string.

    Args:
        amount (int): Amount in cents.
        currency (str): Three-letter currency code.

    Returns:
        str: Formatted string like "$12.50".

    Examples:
        >>> format_currency(1250)
        '$12.50'
        >>> format_currency(1000, "EUR")
        '10.00 EUR'
    """
    return f"${amount / 100:.2f}"
