"""Application configuration."""


def load_settings():
    """Load application settings from environment.

    Type: config

    Fields:
        DEBUG (bool, default=False): Enable debug mode for development.
        SECRET_KEY (str, required, env=APP_SECRET_KEY): Secret key for signing tokens.
        DATABASE_URL (str, required, env=DATABASE_URL): PostgreSQL connection string.
        PORT (int, default=8000): Port to listen on.
        LOG_LEVEL (str, default=INFO): Logging level (DEBUG, INFO, WARNING, ERROR).
    """
    pass
