# CacaoDocs 🍫📚

🌟 **CacaoDocs** is a lightweight Python package that effortlessly extracts API documentation directly from your code's docstrings. 🐍✨ Designed to make generating visually stunning docs quick and easy, it removes the hassle of heavy configuration tools like Sphinx. 🚫📄

I created CacaoDocs because I wanted a simple and beautiful way to produce documentation from docstrings without the repetitive setup. 🛠️💡 It was a cool project idea—I was spending too much time customizing Sphinx to fit my needs, only to redo the whole process for each new project. So, I decided to build something streamlined and visually appealing instead. 🎉📚

With CacaoDocs, you can focus more on your code and less on documentation setup, making your development workflow smoother and more enjoyable! 🚀🔍

## 🚧 Note
CacaoDocs is still under development. It doesn't feature many customization options yet, and you might encounter limitations. Don't expect a fully functional package out of the box—but feel free to contribute and help improve it! 🤝✨

## ✨ Features
- **`doc_type="api"`**: Identify and document your API endpoints (methods and routes). 📡🛠️
- **`doc_type="types"`**: Document data models (classes) that represent objects or entities. 🗃️🔍
- **`doc_type="docs"`**: General documentation for your classes and methods (e.g., core logic or utility functions). 📝🔧
- **Live Preview**: Instantly see your documentation changes in real-time as you code. 👀🔄
- **Multiple Output Formats**: Generate docs in various formats like HTML & Json. 📄📱💻
- **Search Functionality**: Easily find what you need within your documentation with built-in search. 🔍📑
- **Link Generation**: Automatically create links between different parts of your documentation for easy navigation. 🔗🗺️
- **Code Snippet Copying**: Easily copy code examples from your documentation with a single click. 📋💻

## 🚀 Upcoming Features
- **AI-Powered Documentation**: Leverage OpenAI to generate custom, intelligent documentation tailored to your codebase. 🤖📝✨
- **Plugin System**: Extend CacaoDocs functionality with plugins to suit your specific needs. 🧩🔌

---

Join the CacaoDocs community and contribute to making documentation generation easier and more beautiful for everyone! 🌍❤️

![cacaodocs](https://github.com/user-attachments/assets/b2c64a0a-925a-4611-9d27-2976a42e94e9)

## Installation

Install **CacaoDocs** from PyPI:

```bash
pip install cacaodocs
```

## Usage

### 1. Example with a Normal Class

Below is a simple example of how to annotate your methods using the `@CacaoDocs.doc_api` decorator. CacaoDocs will parse your docstrings and generate structured documentation automatically.

```python
from cacaodocs import CacaoDocs

class UserManager:
    def __init__(self):
        """
        Initializes the UserManager with an empty user database.
        """
        self.users = {}
        self.next_id = 1

    @CacaoDocs.doc_api(doc_type="docs", tag="user_manager")
    def create_user(self, username: str, email: str) -> dict:
        """
        Method: create_user
        Version: v1
        Status: Production

        Description:
            Creates a new user with a unique ID, username, and email.

        Args:
            username (str): The username of the new user.
            email (str): The email address of the new user.

        Returns:
            @type{User}
        """
        user_id = self.next_id
        self.users[user_id] = {
            "id": user_id,
            "username": username,
            "email": email
        }
        self.next_id += 1
        return self.users[user_id]

    @CacaoDocs.doc_api(doc_type="docs", tag="user_manager")
    def get_user(self, user_id: int) -> dict:
        """
        Method: get_user
        Version: v1
        Status: Production

        Description:
            Retrieves the details of a user by their unique ID.

        Args:
            user_id (int): The unique identifier of the user.

        Raises:
            KeyError: If the user with the specified ID does not exist.

        Returns:
            @type{dict}: A dictionary containing the user's ID, username, and email.
        """
        try:
            return self.users[user_id]
        except KeyError:
            raise KeyError(f"User with ID {user_id} does not exist.")
```

### 2. Example in a Flask Application

Below is an example `app.py` showing how to set up CacaoDocs within a Flask app. Once your code is annotated with `@CacaoDocs.doc_api`, it will automatically detect endpoints and methods unless you explicitly override them in the docstring.

```python
from flask import Flask, request, jsonify
from cacaodocs import CacaoDocs

# Load the CacaoDocs configuration
CacaoDocs.load_config()

app = Flask(__name__)

@app.route('/api/users', methods=['POST'])
@CacaoDocs.doc_api(doc_type="api", tag="users")
def create_user():
    """
    Method:   POST
    Version:  v1
    Status:   Production
    Last Updated: 2024-04-25

    Description:
        Creates a new user with the provided details.

    Responses:
        201:
            description: "User successfully created."
            example: {"id": 12345, "username": "johndoe"}
        400:
            description: "Bad request due to invalid input."
            example: {"error": "Invalid email format."}
    """
    data = request.json or {}
    try:
        # Assuming `db` is an instance of UserManager or similar
        user = db.create_user(data)
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users/<int:user_id>', methods=['GET'])
@CacaoDocs.doc_api(doc_type="api", tag="users")
def get_user(user_id):
    """
    Endpoint: /api/users_custom/<user_id>
    Method:   GET
    Version:  v1
    Status:   Production
    Last Updated: 2024-04-25

    Description:
        Retrieves the details of a user given their unique ID.

    Args:
        user_id (int): The unique identifier of the user.

    Raises:
        UserNotFoundError: If no user is found with the given `user_id`.

    Responses:
        Data:
            example: @type{User}
    """
    return {"error": "User not found"}, 404

@app.route('/docs', methods=['GET'])
def get_documentation():
    """
    Endpoint: /docs
    Method:   GET
    Version:  v1
    Status:   Production
    Last Updated: 2024-04-25

    Description:
        Returns a JSON object containing metadata for all documented endpoints.
    """
    documentation = CacaoDocs.get_json()
    response = jsonify(documentation)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Enable CORS
    return response, 200

@app.route('/', methods=['GET'])
def get_documentation_html():
    """
    Endpoint: /
    Method:   GET
    Version:  v1
    Status:   Production
    Last Updated: 2024-04-25

    Description:
        Returns an HTML page containing the API documentation.

    Returns:
        200:
            description: "HTML documentation retrieved successfully."
            example: "<html><body>API Documentation</body></html>"
    """
    html_documentation = CacaoDocs.get_html()
    return html_documentation, 200, {'Content-Type': 'text/html'}
```

#### Generating HTML Documentation
If you need to serve the HTML version of your docs directly, you can simply call:

```python
html_documentation = CacaoDocs.get_html()
```

### 3. Example for `types`

You can also document data models or classes with `doc_type="types"`. For example:

```python
from dataclasses import dataclass, asdict
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
    city: 'City'
    country: 'Country'
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
```

## Contributing

CacaoDocs is a work in progress, and any contributions are welcome. Whether it’s:
- Suggesting improvements or new features  
- Submitting bug reports  
- Contributing directly with pull requests  

Feel free to open an issue or create a PR in this repository.

---

**Happy documenting!**
