"""Auto-generated documentation app powered by CacaoDocs + Cacao."""
import json
import cacao as c

# --- Documentation Data ---
_DATA = json.loads('{"modules": [{"name": "app", "full_path": "app", "file_path": "C:\\\\Users\\\\Juan\\\\Documents\\\\GitHub\\\\CacaoDocs\\\\docs\\\\app.py", "docstring": "Sample FastAPI application for testing CacaoDocs doc types.", "classes": [], "functions": [{"name": "get_user", "module": "app", "full_path": "app.get_user", "signature": "(user_id: int, include: str=None)", "docstring": {"summary": "Get a user by their ID.", "description": "", "doc_type": "api", "args": [], "returns": null, "raises": [], "examples": ["    >>> GET /users/42\\n    {\\"id\\": 42, \\"name\\": \\"Alice\\", \\"email\\": \\"alice@example.com\\"}"], "attributes": [], "notes": [], "http_method": "GET", "path": "/users/{user_id}", "path_params": [{"name": "user_id", "type": "int", "description": "The user\'s unique identifier.", "default": null, "required": null}], "query_params": [{"name": "include", "type": "str", "description": "Comma-separated list of fields to include.", "default": null, "required": null}], "request_body": [], "responses": [{"status_code": 200, "description": "", "fields": [{"name": "id", "type": "int", "description": "The user ID."}, {"name": "name", "type": "str", "description": "The user\'s full name."}, {"name": "email", "type": "str", "description": "The user\'s email address."}]}, {"status_code": 404, "description": "", "fields": [{"name": "detail", "type": "str", "description": "User not found error message."}]}], "headers": []}, "is_async": false, "source": "def get_user(user_id: int, include: str = None):\\n    \\"\\"\\"Get a user by their ID.\\n\\n    Type: api\\n\\n    Method: GET\\n    Path: /users/{user_id}\\n\\n    Path Params:\\n        user_id (int): The user\'s unique identifier.\\n\\n    Query Params:\\n        include (str): Comma-separated list of fields to include.\\n\\n    Response (200):\\n        id (int): The user ID.\\n        name (str): The user\'s full name.\\n        email (str): The user\'s email address.\\n\\n    Response (404):\\n        detail (str): User not found error message.\\n\\n    Examples:\\n        >>> GET /users/42\\n        {\\"id\\": 42, \\"name\\": \\"Alice\\", \\"email\\": \\"alice@example.com\\"}\\n    \\"\\"\\"\\n    return {\\"id\\": user_id, \\"name\\": \\"Alice\\", \\"include\\": include}", "line_number": 9, "decorators": ["app.get"], "calls": ["app.get"], "doc_type": "api"}, {"name": "create_user", "module": "app", "full_path": "app.create_user", "signature": "(name: str, email: str)", "docstring": {"summary": "Create a new user account.", "description": "", "doc_type": "api", "args": [], "returns": null, "raises": [], "examples": [], "attributes": [], "notes": [], "http_method": "POST", "path": "/users", "path_params": [], "query_params": [], "request_body": [{"name": "name", "type": "str", "description": "The user\'s full name.", "default": null, "required": true}, {"name": "email", "type": "str", "description": "The user\'s email address.", "default": null, "required": true}], "responses": [{"status_code": 201, "description": "", "fields": [{"name": "id", "type": "int", "description": "The newly created user ID."}, {"name": "name", "type": "str", "description": "The user\'s name."}]}, {"status_code": 400, "description": "", "fields": [{"name": "detail", "type": "str", "description": "Validation error message."}]}], "headers": []}, "is_async": true, "source": "async def create_user(name: str, email: str):\\n    \\"\\"\\"Create a new user account.\\n\\n    Type: api\\n\\n    Method: POST\\n    Path: /users\\n\\n    Request Body:\\n        name (str, required): The user\'s full name.\\n        email (str, required): The user\'s email address.\\n\\n    Response (201):\\n        id (int): The newly created user ID.\\n        name (str): The user\'s name.\\n\\n    Response (400):\\n        detail (str): Validation error message.\\n    \\"\\"\\"\\n    return {\\"id\\": 1, \\"name\\": name, \\"email\\": email}", "line_number": 39, "decorators": ["app.post"], "calls": ["app.post"], "doc_type": "api"}, {"name": "delete_user", "module": "app", "full_path": "app.delete_user", "signature": "(user_id: int)", "docstring": {"summary": "Delete a user permanently.", "description": "", "doc_type": "api", "args": [], "returns": null, "raises": [], "examples": [], "attributes": [], "notes": [], "http_method": "DELETE", "path": "/users/{user_id}", "path_params": [{"name": "user_id", "type": "int", "description": "The user to delete.", "default": null, "required": null}], "query_params": [], "request_body": [], "responses": [{"status_code": 204, "description": "", "fields": []}, {"status_code": 404, "description": "", "fields": [{"name": "detail", "type": "str", "description": "User not found."}]}], "headers": []}, "is_async": false, "source": "def delete_user(user_id: int):\\n    \\"\\"\\"Delete a user permanently.\\n\\n    Type: api\\n\\n    Method: DELETE\\n    Path: /users/{user_id}\\n\\n    Path Params:\\n        user_id (int): The user to delete.\\n\\n    Response (204):\\n\\n    Response (404):\\n        detail (str): User not found.\\n    \\"\\"\\"\\n    return {\\"deleted\\": user_id}", "line_number": 62, "decorators": ["app.delete"], "calls": ["app.delete"], "doc_type": "api"}]}, {"name": "config", "full_path": "config", "file_path": "C:\\\\Users\\\\Juan\\\\Documents\\\\GitHub\\\\CacaoDocs\\\\docs\\\\config.py", "docstring": "Application configuration.", "classes": [], "functions": [{"name": "load_settings", "module": "config", "full_path": "config.load_settings", "signature": "()", "docstring": {"summary": "Load application settings from environment.", "description": "", "doc_type": "config", "args": [], "returns": null, "raises": [], "examples": [], "attributes": [], "notes": [], "config_fields": [{"name": "DEBUG", "type": "bool", "description": "Enable debug mode for development.", "default": "False", "required": false, "env_var": ""}, {"name": "SECRET_KEY", "type": "str", "description": "Secret key for signing tokens.", "default": null, "required": true, "env_var": "APP_SECRET_KEY"}, {"name": "DATABASE_URL", "type": "str", "description": "PostgreSQL connection string.", "default": null, "required": true, "env_var": "DATABASE_URL"}, {"name": "PORT", "type": "int", "description": "Port to listen on.", "default": "8000", "required": false, "env_var": ""}, {"name": "LOG_LEVEL", "type": "str", "description": "Logging level (DEBUG, INFO, WARNING, ERROR).", "default": "INFO", "required": false, "env_var": ""}]}, "is_async": false, "source": "def load_settings():\\n    \\"\\"\\"Load application settings from environment.\\n\\n    Type: config\\n\\n    Fields:\\n        DEBUG (bool, default=False): Enable debug mode for development.\\n        SECRET_KEY (str, required, env=APP_SECRET_KEY): Secret key for signing tokens.\\n        DATABASE_URL (str, required, env=DATABASE_URL): PostgreSQL connection string.\\n        PORT (int, default=8000): Port to listen on.\\n        LOG_LEVEL (str, default=INFO): Logging level (DEBUG, INFO, WARNING, ERROR).\\n    \\"\\"\\"\\n    pass", "line_number": 4, "decorators": [], "calls": [], "doc_type": "config"}]}, {"name": "events", "full_path": "events", "file_path": "C:\\\\Users\\\\Juan\\\\Documents\\\\GitHub\\\\CacaoDocs\\\\docs\\\\events.py", "docstring": "Application event handlers.", "classes": [], "functions": [{"name": "on_user_signup", "module": "events", "full_path": "events.on_user_signup", "signature": "(user_data: dict)", "docstring": {"summary": "Fires when a new user completes registration.", "description": "", "doc_type": "event", "args": [], "returns": null, "raises": [], "examples": ["    >>> {\\"user_id\\": 42, \\"email\\": \\"new@user.com\\", \\"plan\\": \\"pro\\"}"], "attributes": [], "notes": [], "trigger": "When a user submits the signup form and passes validation.", "payload": [{"name": "user_id", "type": "int", "description": "The newly created user ID."}, {"name": "email", "type": "str", "description": "The user\'s email address."}, {"name": "plan", "type": "str", "description": "Selected subscription plan."}]}, "is_async": false, "source": "def on_user_signup(user_data: dict):\\n    \\"\\"\\"Fires when a new user completes registration.\\n\\n    Type: event\\n\\n    Trigger: When a user submits the signup form and passes validation.\\n\\n    Payload:\\n        user_id (int): The newly created user ID.\\n        email (str): The user\'s email address.\\n        plan (str): Selected subscription plan.\\n\\n    Examples:\\n        >>> {\\"user_id\\": 42, \\"email\\": \\"new@user.com\\", \\"plan\\": \\"pro\\"}\\n    \\"\\"\\"\\n    pass", "line_number": 4, "decorators": [], "calls": [], "doc_type": "event"}, {"name": "on_payment_received", "module": "events", "full_path": "events.on_payment_received", "signature": "(payment_data: dict)", "docstring": {"summary": "Fires when a payment is successfully processed.", "description": "", "doc_type": "event", "args": [], "returns": null, "raises": [], "examples": [], "attributes": [], "notes": [], "trigger": "After Stripe webhook confirms payment_intent.succeeded.", "payload": [{"name": "payment_id", "type": "str", "description": "Stripe payment intent ID."}, {"name": "amount", "type": "int", "description": "Amount in cents."}, {"name": "currency", "type": "str", "description": "Three-letter currency code."}, {"name": "user_id", "type": "int", "description": "The paying user\'s ID."}]}, "is_async": false, "source": "def on_payment_received(payment_data: dict):\\n    \\"\\"\\"Fires when a payment is successfully processed.\\n\\n    Type: event\\n\\n    Trigger: After Stripe webhook confirms payment_intent.succeeded.\\n\\n    Payload:\\n        payment_id (str): Stripe payment intent ID.\\n        amount (int): Amount in cents.\\n        currency (str): Three-letter currency code.\\n        user_id (int): The paying user\'s ID.\\n    \\"\\"\\"\\n    pass", "line_number": 22, "decorators": [], "calls": [], "doc_type": "event"}]}, {"name": "models", "full_path": "models", "file_path": "C:\\\\Users\\\\Juan\\\\Documents\\\\GitHub\\\\CacaoDocs\\\\docs\\\\models.py", "docstring": "Data models for the application.", "classes": [{"name": "User", "module": "models", "full_path": "models.User", "docstring": {"summary": "Represents a user in the system.", "description": "", "doc_type": "class", "args": [], "returns": null, "raises": [], "examples": [], "attributes": [{"name": "id", "type": "int", "description": "Unique identifier.", "default": null, "required": null}, {"name": "name", "type": "str", "description": "Full name.", "default": null, "required": null}, {"name": "email", "type": "str", "description": "Email address.", "default": null, "required": null}, {"name": "is_active", "type": "bool", "description": "Whether the user account is active.", "default": null, "required": null}], "notes": []}, "bases": [], "methods": [{"name": "__init__", "module": "models", "signature": "(self, name: str, email: str, is_active: bool=True)", "docstring": {"summary": "Initialize a new User.", "description": "", "doc_type": "function", "args": [{"name": "name", "type": "str", "description": "The user\'s full name.", "default": null, "required": null}, {"name": "email", "type": "str", "description": "The user\'s email address.", "default": null, "required": null}, {"name": "is_active", "type": "bool", "description": "Account status. Defaults to True.", "default": null, "required": null}], "returns": null, "raises": [], "examples": [], "attributes": [], "notes": []}, "is_async": false, "is_classmethod": false, "is_staticmethod": false, "is_property": false, "source": "def __init__(self, name: str, email: str, is_active: bool = True):\\n        \\"\\"\\"Initialize a new User.\\n\\n        Args:\\n            name (str): The user\'s full name.\\n            email (str): The user\'s email address.\\n            is_active (bool): Account status. Defaults to True.\\n        \\"\\"\\"\\n        self.name = name\\n        self.email = email\\n        self.is_active = is_active", "line_number": 14, "decorators": [], "calls": [], "doc_type": "function"}, {"name": "deactivate", "module": "models", "signature": "(self)", "docstring": {"summary": "Deactivate this user account.", "description": "", "doc_type": "function", "args": [], "returns": {"type": "bool", "description": "True if successfully deactivated."}, "raises": [{"type": "ValueError", "description": "If user is already inactive."}], "examples": [], "attributes": [], "notes": []}, "is_async": false, "is_classmethod": false, "is_staticmethod": false, "is_property": false, "source": "def deactivate(self):\\n        \\"\\"\\"Deactivate this user account.\\n\\n        Returns:\\n            bool: True if successfully deactivated.\\n\\n        Raises:\\n            ValueError: If user is already inactive.\\n        \\"\\"\\"\\n        if not self.is_active:\\n            raise ValueError(\\"User is already inactive\\")\\n        self.is_active = False\\n        return True", "line_number": 26, "decorators": [], "calls": ["ValueError"], "doc_type": "function"}, {"name": "to_dict", "module": "models", "signature": "(self) -> dict", "docstring": {"summary": "Convert user to dictionary representation.", "description": "", "doc_type": "function", "args": [], "returns": {"type": "dict", "description": "User data as a dictionary."}, "raises": [], "examples": ["    >>> user = User(\\"Alice\\", \\"alice@example.com\\")\\n    >>> user.to_dict()\\n    {\\"name\\": \\"Alice\\", \\"email\\": \\"alice@example.com\\", \\"is_active\\": True}"], "attributes": [], "notes": []}, "is_async": false, "is_classmethod": false, "is_staticmethod": false, "is_property": false, "source": "def to_dict(self) -> dict:\\n        \\"\\"\\"Convert user to dictionary representation.\\n\\n        Returns:\\n            dict: User data as a dictionary.\\n\\n        Examples:\\n            >>> user = User(\\"Alice\\", \\"alice@example.com\\")\\n            >>> user.to_dict()\\n            {\\"name\\": \\"Alice\\", \\"email\\": \\"alice@example.com\\", \\"is_active\\": True}\\n        \\"\\"\\"\\n        return {\\n            \\"name\\": self.name,\\n            \\"email\\": self.email,\\n            \\"is_active\\": self.is_active,\\n        }", "line_number": 40, "decorators": [], "calls": [], "doc_type": "function"}], "source": "class User:\\n    \\"\\"\\"Represents a user in the system.\\n\\n    Attributes:\\n        id (int): Unique identifier.\\n        name (str): Full name.\\n        email (str): Email address.\\n        is_active (bool): Whether the user account is active.\\n    \\"\\"\\"\\n\\n    def __init__(self, name: str, email: str, is_active: bool = True):\\n        \\"\\"\\"Initialize a new User.\\n\\n        Args:\\n            name (str): The user\'s full name.\\n            email (str): The user\'s email address.\\n            is_active (bool): Account status. Defaults to True.\\n        \\"\\"\\"\\n        self.name = name\\n        self.email = email\\n        self.is_active = is_active\\n\\n    def deactivate(self):\\n        \\"\\"\\"Deactivate this user account.\\n\\n        Returns:\\n            bool: True if successfully deactivated.\\n\\n        Raises:\\n            ValueError: If user is already inactive.\\n        \\"\\"\\"\\n        if not self.is_active:\\n            raise ValueError(\\"User is already inactive\\")\\n        self.is_active = False\\n        return True\\n\\n    def to_dict(self) -> dict:\\n        \\"\\"\\"Convert user to dictionary representation.\\n\\n        Returns:\\n            dict: User data as a dictionary.\\n\\n        Examples:\\n            >>> user = User(\\"Alice\\", \\"alice@example.com\\")\\n            >>> user.to_dict()\\n            {\\"name\\": \\"Alice\\", \\"email\\": \\"alice@example.com\\", \\"is_active\\": True}\\n        \\"\\"\\"\\n        return {\\n            \\"name\\": self.name,\\n            \\"email\\": self.email,\\n            \\"is_active\\": self.is_active,\\n        }", "line_number": 4, "decorators": [], "doc_type": "class"}], "functions": []}, {"name": "utils", "full_path": "utils", "file_path": "C:\\\\Users\\\\Juan\\\\Documents\\\\GitHub\\\\CacaoDocs\\\\docs\\\\utils.py", "docstring": "Utility functions.", "classes": [], "functions": [{"name": "hash_password", "module": "utils", "full_path": "utils.hash_password", "signature": "(password: str, salt: str=None) -> str", "docstring": {"summary": "Hash a password using bcrypt.", "description": "", "doc_type": "function", "args": [{"name": "password", "type": "str", "description": "The plaintext password.", "default": null, "required": null}, {"name": "salt", "type": "str", "description": "Optional salt. Generated if not provided.", "default": null, "required": null}], "returns": {"type": "str", "description": "The hashed password string."}, "raises": [{"type": "ValueError", "description": "If password is empty or too short."}], "examples": ["    >>> hash_password(\\"mysecretpass\\")\\n    \'$2b$12$...\'"], "attributes": [], "notes": []}, "is_async": false, "source": "def hash_password(password: str, salt: str = None) -> str:\\n    \\"\\"\\"Hash a password using bcrypt.\\n\\n    Args:\\n        password (str): The plaintext password.\\n        salt (str): Optional salt. Generated if not provided.\\n\\n    Returns:\\n        str: The hashed password string.\\n\\n    Raises:\\n        ValueError: If password is empty or too short.\\n\\n    Examples:\\n        >>> hash_password(\\"mysecretpass\\")\\n        \'$2b$12$...\'\\n    \\"\\"\\"\\n    if not password or len(password) < 8:\\n        raise ValueError(\\"Password must be at least 8 characters\\")\\n    return f\\"hashed_{password}\\"", "line_number": 4, "decorators": [], "calls": ["ValueError", "len"], "doc_type": "function"}, {"name": "format_currency", "module": "utils", "full_path": "utils.format_currency", "signature": "(amount: int, currency: str=\'USD\') -> str", "docstring": {"summary": "Format an amount in cents to a human-readable currency string.", "description": "", "doc_type": "function", "args": [{"name": "amount", "type": "int", "description": "Amount in cents.", "default": null, "required": null}, {"name": "currency", "type": "str", "description": "Three-letter currency code.", "default": null, "required": null}], "returns": {"type": "str", "description": "Formatted string like \\"$12.50\\"."}, "raises": [], "examples": ["    >>> format_currency(1250)\\n    \'$12.50\'\\n    >>> format_currency(1000, \\"EUR\\")\\n    \'10.00 EUR\'"], "attributes": [], "notes": []}, "is_async": false, "source": "def format_currency(amount: int, currency: str = \\"USD\\") -> str:\\n    \\"\\"\\"Format an amount in cents to a human-readable currency string.\\n\\n    Args:\\n        amount (int): Amount in cents.\\n        currency (str): Three-letter currency code.\\n\\n    Returns:\\n        str: Formatted string like \\"$12.50\\".\\n\\n    Examples:\\n        >>> format_currency(1250)\\n        \'$12.50\'\\n        >>> format_currency(1000, \\"EUR\\")\\n        \'10.00 EUR\'\\n    \\"\\"\\"\\n    return f\\"${amount / 100:.2f}\\"", "line_number": 26, "decorators": [], "calls": [], "doc_type": "function"}]}], "classes": [{"name": "User", "module": "models", "full_path": "models.User", "docstring": {"summary": "Represents a user in the system.", "description": "", "doc_type": "class", "args": [], "returns": null, "raises": [], "examples": [], "attributes": [{"name": "id", "type": "int", "description": "Unique identifier.", "default": null, "required": null}, {"name": "name", "type": "str", "description": "Full name.", "default": null, "required": null}, {"name": "email", "type": "str", "description": "Email address.", "default": null, "required": null}, {"name": "is_active", "type": "bool", "description": "Whether the user account is active.", "default": null, "required": null}], "notes": []}, "bases": [], "methods": [{"name": "__init__", "module": "models", "signature": "(self, name: str, email: str, is_active: bool=True)", "docstring": {"summary": "Initialize a new User.", "description": "", "doc_type": "function", "args": [{"name": "name", "type": "str", "description": "The user\'s full name.", "default": null, "required": null}, {"name": "email", "type": "str", "description": "The user\'s email address.", "default": null, "required": null}, {"name": "is_active", "type": "bool", "description": "Account status. Defaults to True.", "default": null, "required": null}], "returns": null, "raises": [], "examples": [], "attributes": [], "notes": []}, "is_async": false, "is_classmethod": false, "is_staticmethod": false, "is_property": false, "source": "def __init__(self, name: str, email: str, is_active: bool = True):\\n        \\"\\"\\"Initialize a new User.\\n\\n        Args:\\n            name (str): The user\'s full name.\\n            email (str): The user\'s email address.\\n            is_active (bool): Account status. Defaults to True.\\n        \\"\\"\\"\\n        self.name = name\\n        self.email = email\\n        self.is_active = is_active", "line_number": 14, "decorators": [], "calls": [], "doc_type": "function"}, {"name": "deactivate", "module": "models", "signature": "(self)", "docstring": {"summary": "Deactivate this user account.", "description": "", "doc_type": "function", "args": [], "returns": {"type": "bool", "description": "True if successfully deactivated."}, "raises": [{"type": "ValueError", "description": "If user is already inactive."}], "examples": [], "attributes": [], "notes": []}, "is_async": false, "is_classmethod": false, "is_staticmethod": false, "is_property": false, "source": "def deactivate(self):\\n        \\"\\"\\"Deactivate this user account.\\n\\n        Returns:\\n            bool: True if successfully deactivated.\\n\\n        Raises:\\n            ValueError: If user is already inactive.\\n        \\"\\"\\"\\n        if not self.is_active:\\n            raise ValueError(\\"User is already inactive\\")\\n        self.is_active = False\\n        return True", "line_number": 26, "decorators": [], "calls": ["ValueError"], "doc_type": "function"}, {"name": "to_dict", "module": "models", "signature": "(self) -> dict", "docstring": {"summary": "Convert user to dictionary representation.", "description": "", "doc_type": "function", "args": [], "returns": {"type": "dict", "description": "User data as a dictionary."}, "raises": [], "examples": ["    >>> user = User(\\"Alice\\", \\"alice@example.com\\")\\n    >>> user.to_dict()\\n    {\\"name\\": \\"Alice\\", \\"email\\": \\"alice@example.com\\", \\"is_active\\": True}"], "attributes": [], "notes": []}, "is_async": false, "is_classmethod": false, "is_staticmethod": false, "is_property": false, "source": "def to_dict(self) -> dict:\\n        \\"\\"\\"Convert user to dictionary representation.\\n\\n        Returns:\\n            dict: User data as a dictionary.\\n\\n        Examples:\\n            >>> user = User(\\"Alice\\", \\"alice@example.com\\")\\n            >>> user.to_dict()\\n            {\\"name\\": \\"Alice\\", \\"email\\": \\"alice@example.com\\", \\"is_active\\": True}\\n        \\"\\"\\"\\n        return {\\n            \\"name\\": self.name,\\n            \\"email\\": self.email,\\n            \\"is_active\\": self.is_active,\\n        }", "line_number": 40, "decorators": [], "calls": [], "doc_type": "function"}], "source": "class User:\\n    \\"\\"\\"Represents a user in the system.\\n\\n    Attributes:\\n        id (int): Unique identifier.\\n        name (str): Full name.\\n        email (str): Email address.\\n        is_active (bool): Whether the user account is active.\\n    \\"\\"\\"\\n\\n    def __init__(self, name: str, email: str, is_active: bool = True):\\n        \\"\\"\\"Initialize a new User.\\n\\n        Args:\\n            name (str): The user\'s full name.\\n            email (str): The user\'s email address.\\n            is_active (bool): Account status. Defaults to True.\\n        \\"\\"\\"\\n        self.name = name\\n        self.email = email\\n        self.is_active = is_active\\n\\n    def deactivate(self):\\n        \\"\\"\\"Deactivate this user account.\\n\\n        Returns:\\n            bool: True if successfully deactivated.\\n\\n        Raises:\\n            ValueError: If user is already inactive.\\n        \\"\\"\\"\\n        if not self.is_active:\\n            raise ValueError(\\"User is already inactive\\")\\n        self.is_active = False\\n        return True\\n\\n    def to_dict(self) -> dict:\\n        \\"\\"\\"Convert user to dictionary representation.\\n\\n        Returns:\\n            dict: User data as a dictionary.\\n\\n        Examples:\\n            >>> user = User(\\"Alice\\", \\"alice@example.com\\")\\n            >>> user.to_dict()\\n            {\\"name\\": \\"Alice\\", \\"email\\": \\"alice@example.com\\", \\"is_active\\": True}\\n        \\"\\"\\"\\n        return {\\n            \\"name\\": self.name,\\n            \\"email\\": self.email,\\n            \\"is_active\\": self.is_active,\\n        }", "line_number": 4, "decorators": [], "doc_type": "class"}], "functions": [{"name": "load_settings", "module": "config", "full_path": "config.load_settings", "signature": "()", "docstring": {"summary": "Load application settings from environment.", "description": "", "doc_type": "config", "args": [], "returns": null, "raises": [], "examples": [], "attributes": [], "notes": [], "config_fields": [{"name": "DEBUG", "type": "bool", "description": "Enable debug mode for development.", "default": "False", "required": false, "env_var": ""}, {"name": "SECRET_KEY", "type": "str", "description": "Secret key for signing tokens.", "default": null, "required": true, "env_var": "APP_SECRET_KEY"}, {"name": "DATABASE_URL", "type": "str", "description": "PostgreSQL connection string.", "default": null, "required": true, "env_var": "DATABASE_URL"}, {"name": "PORT", "type": "int", "description": "Port to listen on.", "default": "8000", "required": false, "env_var": ""}, {"name": "LOG_LEVEL", "type": "str", "description": "Logging level (DEBUG, INFO, WARNING, ERROR).", "default": "INFO", "required": false, "env_var": ""}]}, "is_async": false, "source": "def load_settings():\\n    \\"\\"\\"Load application settings from environment.\\n\\n    Type: config\\n\\n    Fields:\\n        DEBUG (bool, default=False): Enable debug mode for development.\\n        SECRET_KEY (str, required, env=APP_SECRET_KEY): Secret key for signing tokens.\\n        DATABASE_URL (str, required, env=DATABASE_URL): PostgreSQL connection string.\\n        PORT (int, default=8000): Port to listen on.\\n        LOG_LEVEL (str, default=INFO): Logging level (DEBUG, INFO, WARNING, ERROR).\\n    \\"\\"\\"\\n    pass", "line_number": 4, "decorators": [], "calls": [], "doc_type": "config"}, {"name": "on_user_signup", "module": "events", "full_path": "events.on_user_signup", "signature": "(user_data: dict)", "docstring": {"summary": "Fires when a new user completes registration.", "description": "", "doc_type": "event", "args": [], "returns": null, "raises": [], "examples": ["    >>> {\\"user_id\\": 42, \\"email\\": \\"new@user.com\\", \\"plan\\": \\"pro\\"}"], "attributes": [], "notes": [], "trigger": "When a user submits the signup form and passes validation.", "payload": [{"name": "user_id", "type": "int", "description": "The newly created user ID."}, {"name": "email", "type": "str", "description": "The user\'s email address."}, {"name": "plan", "type": "str", "description": "Selected subscription plan."}]}, "is_async": false, "source": "def on_user_signup(user_data: dict):\\n    \\"\\"\\"Fires when a new user completes registration.\\n\\n    Type: event\\n\\n    Trigger: When a user submits the signup form and passes validation.\\n\\n    Payload:\\n        user_id (int): The newly created user ID.\\n        email (str): The user\'s email address.\\n        plan (str): Selected subscription plan.\\n\\n    Examples:\\n        >>> {\\"user_id\\": 42, \\"email\\": \\"new@user.com\\", \\"plan\\": \\"pro\\"}\\n    \\"\\"\\"\\n    pass", "line_number": 4, "decorators": [], "calls": [], "doc_type": "event"}, {"name": "on_payment_received", "module": "events", "full_path": "events.on_payment_received", "signature": "(payment_data: dict)", "docstring": {"summary": "Fires when a payment is successfully processed.", "description": "", "doc_type": "event", "args": [], "returns": null, "raises": [], "examples": [], "attributes": [], "notes": [], "trigger": "After Stripe webhook confirms payment_intent.succeeded.", "payload": [{"name": "payment_id", "type": "str", "description": "Stripe payment intent ID."}, {"name": "amount", "type": "int", "description": "Amount in cents."}, {"name": "currency", "type": "str", "description": "Three-letter currency code."}, {"name": "user_id", "type": "int", "description": "The paying user\'s ID."}]}, "is_async": false, "source": "def on_payment_received(payment_data: dict):\\n    \\"\\"\\"Fires when a payment is successfully processed.\\n\\n    Type: event\\n\\n    Trigger: After Stripe webhook confirms payment_intent.succeeded.\\n\\n    Payload:\\n        payment_id (str): Stripe payment intent ID.\\n        amount (int): Amount in cents.\\n        currency (str): Three-letter currency code.\\n        user_id (int): The paying user\'s ID.\\n    \\"\\"\\"\\n    pass", "line_number": 22, "decorators": [], "calls": [], "doc_type": "event"}, {"name": "hash_password", "module": "utils", "full_path": "utils.hash_password", "signature": "(password: str, salt: str=None) -> str", "docstring": {"summary": "Hash a password using bcrypt.", "description": "", "doc_type": "function", "args": [{"name": "password", "type": "str", "description": "The plaintext password.", "default": null, "required": null}, {"name": "salt", "type": "str", "description": "Optional salt. Generated if not provided.", "default": null, "required": null}], "returns": {"type": "str", "description": "The hashed password string."}, "raises": [{"type": "ValueError", "description": "If password is empty or too short."}], "examples": ["    >>> hash_password(\\"mysecretpass\\")\\n    \'$2b$12$...\'"], "attributes": [], "notes": []}, "is_async": false, "source": "def hash_password(password: str, salt: str = None) -> str:\\n    \\"\\"\\"Hash a password using bcrypt.\\n\\n    Args:\\n        password (str): The plaintext password.\\n        salt (str): Optional salt. Generated if not provided.\\n\\n    Returns:\\n        str: The hashed password string.\\n\\n    Raises:\\n        ValueError: If password is empty or too short.\\n\\n    Examples:\\n        >>> hash_password(\\"mysecretpass\\")\\n        \'$2b$12$...\'\\n    \\"\\"\\"\\n    if not password or len(password) < 8:\\n        raise ValueError(\\"Password must be at least 8 characters\\")\\n    return f\\"hashed_{password}\\"", "line_number": 4, "decorators": [], "calls": ["ValueError", "len"], "doc_type": "function"}, {"name": "format_currency", "module": "utils", "full_path": "utils.format_currency", "signature": "(amount: int, currency: str=\'USD\') -> str", "docstring": {"summary": "Format an amount in cents to a human-readable currency string.", "description": "", "doc_type": "function", "args": [{"name": "amount", "type": "int", "description": "Amount in cents.", "default": null, "required": null}, {"name": "currency", "type": "str", "description": "Three-letter currency code.", "default": null, "required": null}], "returns": {"type": "str", "description": "Formatted string like \\"$12.50\\"."}, "raises": [], "examples": ["    >>> format_currency(1250)\\n    \'$12.50\'\\n    >>> format_currency(1000, \\"EUR\\")\\n    \'10.00 EUR\'"], "attributes": [], "notes": []}, "is_async": false, "source": "def format_currency(amount: int, currency: str = \\"USD\\") -> str:\\n    \\"\\"\\"Format an amount in cents to a human-readable currency string.\\n\\n    Args:\\n        amount (int): Amount in cents.\\n        currency (str): Three-letter currency code.\\n\\n    Returns:\\n        str: Formatted string like \\"$12.50\\".\\n\\n    Examples:\\n        >>> format_currency(1250)\\n        \'$12.50\'\\n        >>> format_currency(1000, \\"EUR\\")\\n        \'10.00 EUR\'\\n    \\"\\"\\"\\n    return f\\"${amount / 100:.2f}\\"", "line_number": 26, "decorators": [], "calls": [], "doc_type": "function"}], "api_endpoints": [{"name": "get_user", "module": "app", "full_path": "app.get_user", "signature": "(user_id: int, include: str=None)", "docstring": {"summary": "Get a user by their ID.", "description": "", "doc_type": "api", "args": [], "returns": null, "raises": [], "examples": ["    >>> GET /users/42\\n    {\\"id\\": 42, \\"name\\": \\"Alice\\", \\"email\\": \\"alice@example.com\\"}"], "attributes": [], "notes": [], "http_method": "GET", "path": "/users/{user_id}", "path_params": [{"name": "user_id", "type": "int", "description": "The user\'s unique identifier.", "default": null, "required": null}], "query_params": [{"name": "include", "type": "str", "description": "Comma-separated list of fields to include.", "default": null, "required": null}], "request_body": [], "responses": [{"status_code": 200, "description": "", "fields": [{"name": "id", "type": "int", "description": "The user ID."}, {"name": "name", "type": "str", "description": "The user\'s full name."}, {"name": "email", "type": "str", "description": "The user\'s email address."}]}, {"status_code": 404, "description": "", "fields": [{"name": "detail", "type": "str", "description": "User not found error message."}]}], "headers": []}, "is_async": false, "source": "def get_user(user_id: int, include: str = None):\\n    \\"\\"\\"Get a user by their ID.\\n\\n    Type: api\\n\\n    Method: GET\\n    Path: /users/{user_id}\\n\\n    Path Params:\\n        user_id (int): The user\'s unique identifier.\\n\\n    Query Params:\\n        include (str): Comma-separated list of fields to include.\\n\\n    Response (200):\\n        id (int): The user ID.\\n        name (str): The user\'s full name.\\n        email (str): The user\'s email address.\\n\\n    Response (404):\\n        detail (str): User not found error message.\\n\\n    Examples:\\n        >>> GET /users/42\\n        {\\"id\\": 42, \\"name\\": \\"Alice\\", \\"email\\": \\"alice@example.com\\"}\\n    \\"\\"\\"\\n    return {\\"id\\": user_id, \\"name\\": \\"Alice\\", \\"include\\": include}", "line_number": 9, "decorators": ["app.get"], "calls": ["app.get"], "doc_type": "api"}, {"name": "create_user", "module": "app", "full_path": "app.create_user", "signature": "(name: str, email: str)", "docstring": {"summary": "Create a new user account.", "description": "", "doc_type": "api", "args": [], "returns": null, "raises": [], "examples": [], "attributes": [], "notes": [], "http_method": "POST", "path": "/users", "path_params": [], "query_params": [], "request_body": [{"name": "name", "type": "str", "description": "The user\'s full name.", "default": null, "required": true}, {"name": "email", "type": "str", "description": "The user\'s email address.", "default": null, "required": true}], "responses": [{"status_code": 201, "description": "", "fields": [{"name": "id", "type": "int", "description": "The newly created user ID."}, {"name": "name", "type": "str", "description": "The user\'s name."}]}, {"status_code": 400, "description": "", "fields": [{"name": "detail", "type": "str", "description": "Validation error message."}]}], "headers": []}, "is_async": true, "source": "async def create_user(name: str, email: str):\\n    \\"\\"\\"Create a new user account.\\n\\n    Type: api\\n\\n    Method: POST\\n    Path: /users\\n\\n    Request Body:\\n        name (str, required): The user\'s full name.\\n        email (str, required): The user\'s email address.\\n\\n    Response (201):\\n        id (int): The newly created user ID.\\n        name (str): The user\'s name.\\n\\n    Response (400):\\n        detail (str): Validation error message.\\n    \\"\\"\\"\\n    return {\\"id\\": 1, \\"name\\": name, \\"email\\": email}", "line_number": 39, "decorators": ["app.post"], "calls": ["app.post"], "doc_type": "api"}, {"name": "delete_user", "module": "app", "full_path": "app.delete_user", "signature": "(user_id: int)", "docstring": {"summary": "Delete a user permanently.", "description": "", "doc_type": "api", "args": [], "returns": null, "raises": [], "examples": [], "attributes": [], "notes": [], "http_method": "DELETE", "path": "/users/{user_id}", "path_params": [{"name": "user_id", "type": "int", "description": "The user to delete.", "default": null, "required": null}], "query_params": [], "request_body": [], "responses": [{"status_code": 204, "description": "", "fields": []}, {"status_code": 404, "description": "", "fields": [{"name": "detail", "type": "str", "description": "User not found."}]}], "headers": []}, "is_async": false, "source": "def delete_user(user_id: int):\\n    \\"\\"\\"Delete a user permanently.\\n\\n    Type: api\\n\\n    Method: DELETE\\n    Path: /users/{user_id}\\n\\n    Path Params:\\n        user_id (int): The user to delete.\\n\\n    Response (204):\\n\\n    Response (404):\\n        detail (str): User not found.\\n    \\"\\"\\"\\n    return {\\"deleted\\": user_id}", "line_number": 62, "decorators": ["app.delete"], "calls": ["app.delete"], "doc_type": "api"}], "pages": [{"title": "Test Project", "slug": "readme", "content": "<h1 id=\\"test-project\\">Test Project</h1>\\n<p>This is a sample project demonstrating all CacaoDocs doc types.</p>\\n<h2 id=\\"doc-types\\">Doc Types</h2>\\n<ul>\\n<li><strong>function</strong> - Regular Python functions</li>\\n<li><strong>api</strong> - REST API endpoints (auto-detected from FastAPI/Flask decorators)</li>\\n<li><strong>class</strong> - Python classes with methods</li>\\n<li><strong>config</strong> - Configuration and environment variables</li>\\n<li><strong>event</strong> - Webhooks and event handlers</li>\\n</ul>\\n<h2 id=\\"getting-started\\">Getting Started</h2>\\n<p>Install dependencies and run the server:</p>\\n<div class=\\"codehilite\\"><pre><span></span><code>pip<span class=\\"w\\"> </span>install<span class=\\"w\\"> </span>fastapi<span class=\\"w\\"> </span>uvicorn\\nuvicorn<span class=\\"w\\"> </span>app:app<span class=\\"w\\"> </span>--reload\\n</code></pre></div>", "file_path": "C:\\\\Users\\\\Juan\\\\Documents\\\\GitHub\\\\CacaoDocs\\\\docs\\\\README.md", "order": 0}], "config": {"title": "CacaoDocs", "description": "Generate beautiful documentation from Python docstrings", "version": "2.0.0", "theme": {"primary_color": "#8B4513", "secondary_color": "#D2691E", "bg_color": "#faf8f5", "text_color": "#1a202c", "highlight_code_bg_color": "#fff8f0", "highlight_code_border_color": "#8B4513", "sidebar_bg_color": "#ffffff", "sidebar_text_color": "#1a202c", "sidebar_highlight_bg_color": "#8B4513", "sidebar_highlight_text_color": "#ffffff", "secondary_sidebar_bg_color": "#f5f0eb", "secondary_sidebar_text_color": "#1a202c", "secondary_sidebar_highlight_bg_color": "#8B4513", "secondary_sidebar_highlight_text_color": "#ffffff", "home_page_welcome_bg_1": "#8B4513", "home_page_welcome_bg_2": "#D2691E", "home_page_welcome_text_color": "#ffffff", "home_page_card_bg_color": "#ffffff", "home_page_card_text_color": "#1a202c", "code_bg_color": "#f5f0eb"}, "logo_url": "", "github_url": "https://github.com/jhd3197/CacaoDocs", "footer_text": "Built with CacaoDocs", "exclude_patterns": [".venv", ".tox", "node_modules", ".git", ".pytest_cache", "venv", "*.egg-info", "dist", "__pypackages__", "__pycache__", "build"], "verbose": true}}')

_PAGES = _DATA["pages"]
_CONFIG = _DATA["config"]


def _has_docstring(item):
    """Check if an item has a meaningful docstring."""
    ds = item.get("docstring")
    if not ds:
        return False
    if isinstance(ds, dict):
        return bool(ds.get("summary") or ds.get("description"))
    if isinstance(ds, str):
        return bool(ds.strip())
    return False


# Filter: only items with actual docstrings
_ALL_MODULES = _DATA["modules"]
_CONTENT_MODULES = [m for m in _ALL_MODULES
                    if m.get("docstring")
                    or any(_has_docstring(c) for c in m.get("classes", []))
                    or any(_has_docstring(f) for f in m.get("functions", []))]

_CLASSES = [c for c in _DATA["classes"] if _has_docstring(c)]
_FUNCTIONS = [f for f in _DATA["functions"] if _has_docstring(f)]
_API_ENDPOINTS = [e for e in _DATA.get("api_endpoints", []) if _has_docstring(e)]

# Filter methods within classes
for cls in _CLASSES:
    cls["methods"] = [m for m in cls.get("methods", [])
                      if _has_docstring(m) or m["name"] == "__init__"]

for mod in _CONTENT_MODULES:
    mod["classes"] = [c for c in mod.get("classes", []) if _has_docstring(c)]
    mod["functions"] = [f for f in mod.get("functions", []) if _has_docstring(f)]
    for cls in mod["classes"]:
        cls["methods"] = [m for m in cls.get("methods", [])
                          if _has_docstring(m) or m["name"] == "__init__"]

# --- App Config ---
c.config(
    title='CacaoDocs',
    theme='light',
)





# --- Helpers ---

_METHOD_COLORS = {
    "GET": "success",
    "POST": "info",
    "PUT": "warning",
    "PATCH": "warning",
    "DELETE": "danger",
    "OPTIONS": "default",
    "HEAD": "default",
}


def _render_args_table(args, label="Parameters"):
    """Render a list of args as a table."""
    if not args:
        return
    c.spacer(3)
    c.title(label, level=4)
    c.spacer(1)
    table_data = []
    for arg in args:
        row = {"Name": arg["name"]}
        if arg.get("type"):
            row["Type"] = arg["type"]
        row["Description"] = arg.get("description", "")
        if arg.get("default"):
            row["Default"] = arg["default"]
        if arg.get("required"):
            row["Required"] = "Yes"
        if arg.get("env_var"):
            row["Env Var"] = arg["env_var"]
        table_data.append(row)
    c.table(table_data, paginate=False, sortable=False)


def _render_docstring(docstring):
    """Render a parsed docstring."""
    if docstring.get("summary"):
        c.text(docstring["summary"], size="lg")

    if docstring.get("description"):
        c.spacer(2)
        c.text(docstring["description"], color="muted")

    doc_type = docstring.get("doc_type", "function")

    # --- API-specific rendering ---
    if doc_type == "api":
        # Method + Path badge
        method = docstring.get("http_method", "")
        path = docstring.get("path", "")
        if method or path:
            c.spacer(2)
            with c.row(gap=2, wrap=True):
                if method:
                    c.badge(method, color=_METHOD_COLORS.get(method, "default"))
                if path:
                    c.code(path, language="text")

        _render_args_table(docstring.get("path_params", []), "Path Parameters")
        _render_args_table(docstring.get("query_params", []), "Query Parameters")
        _render_args_table(docstring.get("request_body", []), "Request Body")

        # Headers
        headers = docstring.get("headers", [])
        if headers:
            c.spacer(3)
            c.title("Headers", level=4)
            c.spacer(1)
            table_data = []
            for h in headers:
                row = {"Name": h["name"], "Description": h.get("description", "")}
                if h.get("required"):
                    row["Required"] = "Yes"
                if h.get("example"):
                    row["Example"] = h["example"]
                table_data.append(row)
            c.table(table_data, paginate=False, sortable=False)

        # Responses
        responses = docstring.get("responses", [])
        if responses:
            c.spacer(3)
            c.title("Responses", level=4)
            c.spacer(1)
            for resp in responses:
                status = resp.get("status_code", "")
                desc = resp.get("description", "")
                color = "success" if 200 <= status < 300 else "warning" if 300 <= status < 400 else "danger"
                with c.card(f"{status} {desc}"):
                    c.badge(str(status), color=color)
                    if desc:
                        c.text(desc, color="muted")
                    fields = resp.get("fields", [])
                    if fields:
                        _render_args_table(fields, "Fields")

    # --- Event-specific rendering ---
    elif doc_type == "event":
        trigger = docstring.get("trigger", "")
        if trigger:
            c.spacer(2)
            c.title("Trigger", level=4)
            c.text(trigger)

        payload = docstring.get("payload", [])
        if payload:
            _render_args_table(payload, "Payload")

    # --- Config-specific rendering ---
    elif doc_type == "config":
        config_fields = docstring.get("config_fields", [])
        if config_fields:
            _render_args_table(config_fields, "Configuration Fields")

    # --- Standard function/class rendering ---
    _render_args_table(docstring.get("args", []), "Parameters")

    # Returns
    ret = docstring.get("returns")
    if ret:
        c.spacer(3)
        c.title("Returns", level=4)
        c.spacer(1)
        parts = []
        if ret.get("type"):
            parts.append(ret["type"])
        if ret.get("description"):
            parts.append(ret["description"])
        c.text(" — ".join(parts) if parts else "")

    # Raises
    raises = docstring.get("raises", [])
    if raises:
        c.spacer(3)
        c.title("Raises", level=4)
        c.spacer(1)
        for r in raises:
            c.text(f'{r["type"]}: {r.get("description", "")}')

    # Attributes
    _render_args_table(docstring.get("attributes", []), "Attributes")

    # Examples
    examples = docstring.get("examples", [])
    if examples:
        c.spacer(3)
        c.title("Examples", level=4)
        c.spacer(1)
        for ex in examples:
            c.code(ex, language="python")

    # Notes
    notes = docstring.get("notes", [])
    if notes:
        c.spacer(3)
        for note in notes:
            c.alert(note, type="info")

    # Custom sections
    custom = docstring.get("custom_sections", {})
    for section_name, section_content in custom.items():
        c.spacer(3)
        c.title(section_name, level=4)
        c.spacer(1)
        c.text(section_content)


def _render_function_block(func):
    """Render a function as a section."""
    name = func["name"]
    sig = func.get("signature", "()")
    decorators = func.get("decorators", [])
    doc_type = func.get("doc_type", "function")

    c.divider()
    c.spacer(2)

    # For API endpoints, show method + path as header
    ds = func.get("docstring", {})
    if doc_type == "api":
        method = ds.get("http_method", "")
        path = ds.get("path", "")
        if method or path:
            with c.row(gap=2, wrap=True):
                if method:
                    c.badge(method, color=_METHOD_COLORS.get(method, "default"))
                c.text(f"{path or name}", size="lg")
        else:
            c.code(f"def {name}{sig}", language="python")
    else:
        prefix = "async " if func.get("is_async") else ""
        c.code(f"{prefix}def {name}{sig}", language="python")

    # Badges row
    badges = []
    if doc_type != "function":
        badges.append((doc_type, "info"))
    for dec in decorators:
        badges.append(("@" + dec, "default"))
    if func.get("is_async"):
        badges.append(("async", "warning"))
    if func.get("is_classmethod"):
        badges.append(("classmethod", "info"))
    if func.get("is_staticmethod"):
        badges.append(("staticmethod", "info"))
    if func.get("is_property"):
        badges.append(("property", "success"))

    if badges:
        c.spacer(1)
        with c.row(gap=2, wrap=True):
            for label, color in badges:
                c.badge(label, color=color)

    c.spacer(2)
    _render_docstring(ds)

    # Calls
    calls = func.get("calls", [])
    if calls:
        c.spacer(2)
        c.title("Calls", level=4)
        c.spacer(1)
        with c.row(gap=2, wrap=True):
            for call_name in calls:
                c.badge(call_name, color="default")

    # Source
    if func.get("source"):
        c.spacer(2)
        with c.tabs():
            with c.tab("src_" + name, "Source Code"):
                c.code(func["source"], language="python")

    c.spacer(3)


def _render_class_detail(cls):
    """Render full class documentation."""
    bases_str = ""
    if cls.get("bases"):
        bases_str = f'({", ".join(cls["bases"])})'

    c.code(f'class {cls["name"]}{bases_str}', language="python")

    if cls.get("decorators"):
        c.spacer(1)
        with c.row(gap=2, wrap=True):
            for dec in cls["decorators"]:
                c.badge(f"@{dec}", color="info")

    c.spacer(2)
    _render_docstring(cls["docstring"])

    init_method = next((m for m in cls.get("methods", []) if m["name"] == "__init__"), None)
    if init_method:
        c.spacer(3)
        c.title("Constructor", level=3)
        _render_function_block(init_method)

    methods = [m for m in cls.get("methods", []) if not m["name"].startswith("_")]
    if methods:
        c.spacer(2)
        c.title("Methods", level=3)
        for method in methods:
            _render_function_block(method)

    private_methods = [m for m in cls.get("methods", [])
                       if m["name"].startswith("_") and m["name"] != "__init__"]
    if private_methods:
        c.spacer(2)
        with c.tabs():
            with c.tab("private", f"Private Methods ({len(private_methods)})"):
                for method in private_methods:
                    _render_function_block(method)


# =============================================================================
# Build the App
# =============================================================================

_default_key = "home"

with c.app_shell(brand='CacaoDocs', default=_default_key, theme_dark="dark", theme_light="light"):
    with c.nav_sidebar():
        c.nav_item("Home", key="home", icon="home")

        if _CONTENT_MODULES:
            with c.nav_group("Modules", icon="folder"):
                for mod in _CONTENT_MODULES:
                    label = mod["full_path"] if mod["name"] == "__init__" else mod["name"]
                    badge_count = str(len(mod.get("classes", [])) + len(mod.get("functions", [])))
                    c.nav_item(label, key=f"mod_{mod['full_path']}", icon="file", badge=badge_count)

        if _CLASSES:
            c.nav_item("Types", key="types_ref", icon="box",
                        badge=str(len(_CLASSES)))

        # API Endpoints section
        if _API_ENDPOINTS:
            c.nav_item("API Reference", key="api_ref", icon="code",
                        badge=str(len(_API_ENDPOINTS)))

        c.nav_item("Call Map", key="callmap", icon="code")

        if _PAGES:
            with c.nav_group("Pages", icon="book"):
                for page in _PAGES:
                    c.nav_item(page["title"], key=f"page_{page['slug']}", icon="book")



    with c.shell_content():
        # --- Home ---
        with c.nav_panel("home"):
            c.title('CacaoDocs')
            if 'Generate beautiful documentation from Python docstrings':
                c.text('Generate beautiful documentation from Python docstrings', size="lg", color="muted")
            c.spacer(4)

            with c.row(wrap=True, gap=4):
                c.metric("Modules", len(_CONTENT_MODULES))
                c.metric("Classes", len(_CLASSES))
                c.metric("Functions", len(_FUNCTIONS))
                if _API_ENDPOINTS:
                    c.metric("API Endpoints", len(_API_ENDPOINTS))
                if _PAGES:
                    c.metric("Pages", len(_PAGES))

            if '2.0.0':
                c.spacer(3)
                c.badge(f"v{'2.0.0'}", color="info")

            # Quick overview
            if _CONTENT_MODULES:
                c.spacer(4)
                c.title("Modules", level=3)
                c.spacer(2)
                for mod in _CONTENT_MODULES:
                    label = mod["full_path"] if mod["name"] == "__init__" else mod["name"]
                    with c.card(label):
                        if mod.get("docstring"):
                            first_line = mod["docstring"].split("\n")[0].strip()
                            c.text(first_line, color="muted")
                        with c.row(gap=2):
                            if mod.get("classes"):
                                c.badge(f'{len(mod["classes"])} classes', color="info")
                            if mod.get("functions"):
                                c.badge(f'{len(mod["functions"])} functions', color="default")

            # API overview on home
            if _API_ENDPOINTS:
                c.spacer(4)
                c.title("API Endpoints", level=3)
                c.spacer(2)
                table_data = []
                for ep in _API_ENDPOINTS:
                    ds = ep.get("docstring", {})
                    method = ds.get("http_method", "")
                    path = ds.get("path", "")
                    table_data.append({
                        "Method": method,
                        "Path": path,
                        "Summary": ds.get("summary", ""),
                    })
                c.table(table_data, paginate=False)

        # --- Module Panels ---
        for mod in _CONTENT_MODULES:
            with c.nav_panel(f"mod_{mod['full_path']}"):
                mod_label = mod["full_path"] if mod["name"] == "__init__" else mod["name"]
                c.title(mod_label, level=2)

                if mod.get("file_path"):
                    c.text(mod["file_path"], size="sm", color="muted")

                if mod.get("docstring"):
                    c.spacer(2)
                    c.text(mod["docstring"])

                if mod.get("classes"):
                    c.spacer(4)
                    c.title("Classes", level=3)
                    c.spacer(2)
                    for cls in mod["classes"]:
                        with c.card(f'class {cls["name"]}'):
                            _render_docstring(cls["docstring"])
                            pub_methods = [m for m in cls.get("methods", []) if not m["name"].startswith("_")]
                            if pub_methods:
                                c.spacer(2)
                                c.badge(f"{len(pub_methods)} methods", color="info")

                if mod.get("functions"):
                    c.spacer(4)
                    c.title("Functions", level=3)
                    for func in mod["functions"]:
                        _render_function_block(func)

        # --- Types Reference Panel ---
        if _CLASSES:
            with c.nav_panel("types_ref"):
                with c.layout("sidebar", sidebar_width="260px") as _tl:
                    with _tl.side():
                        c.title("Types", level=3)
                        c.spacer(2)
                        # Group classes by module
                        _cls_by_mod = {}
                        for cls in _CLASSES:
                            mod = cls.get("module", "")
                            _cls_by_mod.setdefault(mod, []).append(cls)

                        with c.subnav(searchable=True):
                            for mod, classes in _cls_by_mod.items():
                                if mod:
                                    c.subnav_group(mod)
                                for cls in classes:
                                    method_count = len(cls.get("methods", []))
                                    c.subnav_item(
                                        cls["name"],
                                        badge=str(method_count),
                                        target=f'type_{cls["full_path"]}',
                                    )

                    with _tl.main():
                        c.title("Types Reference", level=2)
                        c.text(f"{len(_CLASSES)} classes across the codebase.", color="muted")
                        c.spacer(4)

                        for cls in _CLASSES:
                            c.raw_html(f'<div id="type_{cls["full_path"]}"></div>')
                            with c.card():
                                _render_class_detail(cls)
                            c.spacer(3)

        # --- API Reference Panel ---
        if _API_ENDPOINTS:
            with c.nav_panel("api_ref"):
                with c.layout("sidebar", sidebar_width="260px") as _al:
                    with _al.side():
                        c.title("Endpoints", level=3)
                        c.spacer(2)
                        # Group by path prefix (first path segment)
                        _ep_groups = {}
                        for ep in _API_ENDPOINTS:
                            ds = ep.get("docstring", {})
                            path = ds.get("path", "")
                            prefix = "/" + path.strip("/").split("/")[0] if path.strip("/") else "/"
                            _ep_groups.setdefault(prefix, []).append(ep)

                        _TAG_COLORS = {"GET": "success", "POST": "info", "PUT": "warning", "PATCH": "warning", "DELETE": "danger"}
                        with c.subnav(searchable=True):
                            for prefix, eps in _ep_groups.items():
                                c.subnav_group(prefix)
                                for ep in eps:
                                    ds = ep.get("docstring", {})
                                    method = ds.get("http_method", "GET")
                                    path = ds.get("path", ep["name"])
                                    c.subnav_item(
                                        path,
                                        tag=method,
                                        tag_color=_TAG_COLORS.get(method),
                                        target=f'ep_{ep["full_path"]}',
                                    )

                    with _al.main():
                        c.title("API Reference", level=2)
                        c.text(f"{len(_API_ENDPOINTS)} endpoints.", color="muted")
                        c.spacer(3)

                        # Summary table
                        _method_counts = {}
                        for ep in _API_ENDPOINTS:
                            m = ep.get("docstring", {}).get("http_method", "GET")
                            _method_counts[m] = _method_counts.get(m, 0) + 1
                        with c.row(gap=3, wrap=True):
                            for m, count in sorted(_method_counts.items()):
                                c.metric(m, count)
                        c.spacer(4)

                        for ep in _API_ENDPOINTS:
                            ds = ep.get("docstring", {})
                            method = ds.get("http_method", "")
                            path = ds.get("path", "")

                            c.raw_html(f'<div id="ep_{ep["full_path"]}"></div>')
                            with c.card():
                                # Header with method badge + path
                                with c.row(gap=3, wrap=True):
                                    if method:
                                        c.badge(method, color=_METHOD_COLORS.get(method, "default"))
                                    c.title(path or ep["name"], level=3)

                                if ep.get("module"):
                                    c.text(f'{ep["module"]}.{ep["name"]}', size="sm", color="muted")

                                c.spacer(2)
                                _render_docstring(ds)

                                # Source
                                if ep.get("source"):
                                    c.spacer(3)
                                    with c.tabs():
                                        with c.tab("src_" + ep["name"], "Source Code"):
                                            c.code(ep["source"], language="python")
                            c.spacer(3)

        # --- Call Map Panel ---
        with c.nav_panel("callmap"):
            c.title("Call Map", level=2)
            c.text("Function and method call relationships across the codebase.", color="muted")
            c.spacer(3)

            _all_known = set()
            _call_entries = []

            for func in _FUNCTIONS:
                _all_known.add(func["full_path"])
                _all_known.add(func["name"])
            for ep in _API_ENDPOINTS:
                _all_known.add(ep["full_path"])
                _all_known.add(ep["name"])
            for cls in _CLASSES:
                _all_known.add(cls["full_path"])
                for m in cls.get("methods", []):
                    _all_known.add(f'{cls["full_path"]}.{m["name"]}')
                    _all_known.add(m["name"])

            all_funcs = _FUNCTIONS + _API_ENDPOINTS
            for func in all_funcs:
                calls = func.get("calls", [])
                if calls:
                    internal = [c for c in calls if c in _all_known or c.split(".")[-1] in _all_known]
                    external = [c for c in calls if c not in internal]
                    if internal or external:
                        _call_entries.append({
                            "caller": func["full_path"],
                            "internal": internal,
                            "external": external,
                        })

            for cls in _CLASSES:
                for m in cls.get("methods", []):
                    calls = m.get("calls", [])
                    if calls:
                        caller = f'{cls["full_path"]}.{m["name"]}'
                        internal = [c for c in calls if c in _all_known or c.split(".")[-1] in _all_known]
                        external = [c for c in calls if c not in internal]
                        if internal or external:
                            _call_entries.append({
                                "caller": caller,
                                "internal": internal,
                                "external": external,
                            })

            if _call_entries:
                table_data = []
                for entry in _call_entries:
                    table_data.append({
                        "Caller": entry["caller"],
                        "Internal Calls": ", ".join(entry["internal"]) if entry["internal"] else "—",
                        "External Calls": str(len(entry["external"])),
                    })
                c.table(table_data, searchable=True, page_size=20)

                c.spacer(4)
                c.title("Details", level=3)
                c.spacer(2)
                for entry in _call_entries:
                    if entry["internal"]:
                        with c.card(entry["caller"]):
                            c.title("Calls (internal)", level=4)
                            with c.row(gap=2, wrap=True):
                                for call_name in entry["internal"]:
                                    c.badge(call_name, color="info")
                            if entry["external"]:
                                c.spacer(2)
                                c.title("Calls (external)", level=4)
                                with c.row(gap=2, wrap=True):
                                    for call_name in entry["external"][:15]:
                                        c.badge(call_name, color="default")
                                    if len(entry["external"]) > 15:
                                        c.text(f'... and {len(entry["external"]) - 15} more', size="sm", color="muted")
            else:
                c.text("No call relationships found.", color="muted")

        # --- Page Panels ---
        for page in _PAGES:
            with c.nav_panel(f"page_{page['slug']}"):
                c.title(page["title"], level=2)
                c.spacer(2)
                c.html(page.get("content", ""))


