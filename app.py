# app.py
import json
from flask import Flask, request, jsonify
from flask.json import JSONEncoder
from cacaodocs import CacaoDocs
from models.user import User, Address
from models.database import MockDatabase
from models.locations import City, Country
from typing import Union

class CustomJSONEncoder(JSONEncoder):
    """Custom JSON encoder for Flask."""
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return super().default(obj)

# Load configuration from file
CacaoDocs.load_config()

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
db = MockDatabase()

@app.route('/api/users', methods=['POST'])
@CacaoDocs.doc_api(doc_type="api", tag="users")
def create_user():
    """
    Endpoint: /api/users
    Method:   POST
    Version:  v1
    Status:   Production
    Last Updated: 2024-04-25

    Description:
        Creates a new user with the provided details.

    Args:
        None

    JSON Body:
        {
            "username": "johndoe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "addresses": [
                {
                    "street": "123 Main St",
                    "city": {
                        "name": "Boston",
                        "state": "Massachusetts",
                        "country_code": "US",
                        "latitude": 42.3601,
                        "longitude": -71.0589
                    },
                    "country": {
                        "code": "US",
                        "name": "United States",
                        "phone_code": "+1"
                    },
                    "postal_code": "02101"
                }
            ]
        }

    Returns:
        @type{User}: The created user record with full address details.
    """
    data = request.json or {}
    try:
        user = db.create_user(data)
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users/<int:user_id>', methods=['GET'])
@CacaoDocs.doc_api(doc_type="api", tag="users")
def get_user(user_id):
    """
    Endpoint: /api/users/<user_id>
    Method:   GET
    Version:  v1
    Status:   Production
    Last Updated: 2024-04-25

    Description:
        Retrieves the details of a user given their unique ID.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        @type{User}: The complete user record with all associated data.

    Raises:
        UserNotFoundError: If no user is found with the given `user_id`.
    """
    if user := db.get_user(user_id):
        return user  # Now Flask will use our custom JSON encoder
    return {"error": "User not found"}, 404

@app.route('/api/users/<int:user_id>/email', methods=['PATCH'])
@CacaoDocs.doc_api(doc_type="api", tag="users")
def update_user_email(user_id):
    """
    Endpoint: /api/users/<user_id>/email
    Method:   PATCH
    Version:  v1
    Status:   In Review
    Last Updated: 2024-04-25

    Description:
        Updates the email address of an existing user.

    Args:
        user_id (int): The unique identifier of the user.

    JSON Body:
        {
            "email": "newemail@example.com"
        }

    Returns:
        @type{User}: The updated user record.

    Raises:
        UserNotFoundError: If no user is found with the given `user_id`.
    """
    try:
        user = db.update_user_email(user_id, request.json.get("email"))
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@CacaoDocs.doc_api(doc_type="api", tag="users")
def delete_user(user_id):
    """
    Endpoint: /api/users/<user_id>
    Method:   DELETE
    Version:  v1
    Status:   In Review
    Last Updated: 2024-04-25

    Description:
        Deletes an existing user from the system.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        @type{dict}: A message confirming deletion.

    Raises:
        UserNotFoundError: If no user is found with the given `user_id`.
    """
    try:
        db.delete_user(user_id)
        return jsonify({"message": f"User {user_id} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/users', methods=['GET'])
@CacaoDocs.doc_api(doc_type="api", tag="users")
def list_users():
    """
    Endpoint: /api/users
    Method:   GET
    Version:  v1
    Status:   Production
    Last Updated: 2024-04-25

    Description:
        Retrieves a list of all users in the system.

    Args:
        None

    Returns:
        @type{list[User]}: A list of user records.
    """
    users = [user.to_dict() for user in db.list_users()]
    return jsonify(users), 200

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

    Args:
        None

    Returns:
        @type{dict}: The documentation registry.
    """
    documentation = CacaoDocs.get_json()
    return jsonify(documentation), 200

@app.route('/docs/html', methods=['GET'])
def get_documentation_html():
    """
    Endpoint: /docs/html
    Method:   GET
    Version:  v1
    Status:   Production
    Last Updated: 2024-04-25

    Description:
        Returns an HTML page containing the API documentation.

    Args:
        None

    Returns:
        @type{str}: HTML documentation string
    """
    html_documentation = CacaoDocs.get_html()
    return html_documentation, 200, {'Content-Type': 'text/html'}

if __name__ == '__main__':
    app.run(debug=True)
