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
- **Global Search Functionality with FlexSearch**: Easily find what you need within your documentation with built-in search. 🔍📑
  <img width="336" alt="image" src="https://github.com/user-attachments/assets/21c8e836-5ec6-4364-9fb7-56ff8afeecd3" />

- **Link Generation**: Automatically create links between different parts of your documentation for easy navigation. 🔗🗺️
- **Code Snippet Copying**: Easily copy code examples from your documentation with a single click. 📋💻
- **API Status Tracking**: Display the current status of each API endpoint, indicating whether it's under development or in production. 🛠️🔄
- **ER Diagram for the Types Page**: Visual representation of the data models and their relationships within the Types documentation. 📊📚
- **Recent Changes View Based on "Last Updated"**: Easily view the latest updates and modifications to your documentation based on the "Last Updated" timestamps. 🕒🔍
- **Analytics Integration**: Track documentation usage with Google Analytics 4 and Microsoft Clarity. 📊🔍
- **Usage Insights**: Understand how users interact with your documentation through heatmaps and session recordings. 👥📈

## 🚀 Upcoming Features
- **AI-Powered Documentation**: Leverage OpenAI to generate custom, intelligent documentation tailored to your codebase. 🤖📝✨
- **Plugin System**: Extend CacaoDocs functionality with plugins to suit your specific needs. 🧩🔌

---

Join the CacaoDocs community and contribute to making documentation generation easier and more beautiful for everyone! 🌍❤️

![cacaoDocsV2](https://github.com/user-attachments/assets/b0a6709f-c5d5-4aab-85a2-13ed540ba7ec)

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

### 4. API Status Tracking

CacaoDocs now includes **API Status Tracking**, allowing you to indicate whether each endpoint is under development or in production. This helps in maintaining clarity about the stability and readiness of different parts of your API.

**Example:**

```python
@CacaoDocs.doc_api(doc_type="api", tag="users")
def delete_user(user_id: int):
    """
    Endpoint: /api/users/<user_id>
    Method:   DELETE
    Version:  v1
    Status:   Under Development
    Last Updated: 2024-05-10

    Description:
        Deletes a user by their unique ID.

    Args:
        user_id (int): The unique identifier of the user to delete.

    Responses:
        200:
            description: "User successfully deleted."
        404:
            description: "User not found."
    """
    # Implementation goes here
    pass
```

### 5. ER Diagram for the Types Page

To provide a clear understanding of the relationships between different data models, CacaoDocs now supports embedding an **ER Diagram** within the Types documentation.

**Example:**

![ER_Diagram](https://github.com/user-attachments/assets/d78a4406-9063-464b-8903-da7160017af5)

*Figure 1: ER Diagram for the Types Page*

### 6. Recent Changes View Based on "Last Updated"

CacaoDocs introduces a **Recent Changes View** that allows you to track the latest modifications to your documentation based on the "Last Updated" timestamps.

**Example:**

```json
{
    "endpoints": [
        {
            "path": "/api/users",
            "method": "POST",
            "last_updated": "2024-04-25",
            "status": "Production"
        },
        {
            "path": "/api/users/<int:user_id>",
            "method": "GET",
            "last_updated": "2024-04-25",
            "status": "Production"
        },
        {
            "path": "/api/users/<user_id>",
            "method": "DELETE",
            "last_updated": "2024-05-10",
            "status": "Under Development"
        }
    ],
    "types": [
        {
            "name": "Address",
            "last_updated": "2024-03-15"
        }
    ]
}
```

This JSON structure allows developers to quickly identify the most recently updated parts of the documentation, ensuring they stay informed about the latest changes.

## Contributing

CacaoDocs is a work in progress, and any contributions are welcome. Whether it’s:
- Suggesting improvements or new features  
- Submitting bug reports  
- Contributing directly with pull requests  

Feel free to open an issue or create a PR in this repository.

---

**Happy documenting!**

---

# Screenshots
<img width="695" alt="image" src="https://github.com/user-attachments/assets/5dcac8db-8fe6-44d6-b683-b4afc37a59e2" />

*Figure 2: API Status Tracking*

<img width="809" alt="image" src="https://github.com/user-attachments/assets/fb946c05-48c3-4466-8578-5e266bc111ba" />

*Figure 3: Recent Changes View Based on "Last Updated"*

---

Feel free to customize the image URLs and additional sections as needed to fit your project's structure and resources.
