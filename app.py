# app.py

from flask import Flask, request, jsonify, render_template, json
from models.database import MockDatabase

from cacaodocs import CacaoDocs

CacaoDocs.load_config()

import pkg_test


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for Flask."""
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return super().default(obj)

# Load configuration from file

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
db = MockDatabase()

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
            example:{"id": 12345,"username": "johndoe"}
        400:
            description: "Bad request due to invalid input."
            example:{"error": "Invalid email format."}
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
    Endpoint: /api/users_custom/<user_id>
    Method:   GET
    Version:  v1
    Status:   Production
    Last Updated: 2024-02-15

    Description:
        Retrieves the details of a user given their unique ID.

    Args:
        user_id (int): The unique identifier of the user.

    Raises:
        UserNotFoundError: If no user is found with the given `user_id`.

    Responses:
        Data:
            example:@type{User}
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
    Last Updated: 2024-01-22

    Description:
        Updates the email address of an existing user.

    Args:
        user_id (int): The unique identifier of the user.

    Raises:
        UserNotFoundError: If no user is found with the given `user_id`.

    Responses:
        Data:
            example: "{"id": 12345,"username": "johndoe"}"
        200:
            description: "User email updated successfully."
            example:{"id": 12345,"username": "johndoe"}
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
    Last Updated: 2024-04-24

    Description:
        Deletes an existing user from the system.

    Args:
        user_id (int): The unique identifier of the user.

    Raises:
        UserNotFoundError: If no user is found with the given `user_id`.

    Responses:
        200:
            example: {"message": "User 12345 deleted successfully."}
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
    Status:   Planned
    Last Updated: 2025-01-02

    Description:
        Retrieves a list of all users in the system.

    Responses:
        200:
            description: "List of users retrieved successfully."
            example: [{"id": 12345,"username": "johndoe"}]
        304:
            description: "No users found in the system."
            example: {"message": "No users found."}
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
    Last Updated: 2024-02-15

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
    Last Updated: 2024-02-15

    Description:
        Returns an HTML page containing the API documentation.

    Returns:
        200:
            description: "HTML documentation retrieved successfully."
            example: "<html><body>API Documentation</body></html>"
    """
    html_documentation = CacaoDocs.get_html()
    return html_documentation, 200, {'Content-Type': 'text/html'}

@app.route('/docs-one', methods=['GET'])
def get_documentation_one():
    """
    Endpoint: /docs-one
    Method:   GET
    Version:  v1
    Status:   Production
    Last Updated: 2024-02-17

    Description:
        Returns a JSON object containing one configuration from each category.
    """
    documentation_one = CacaoDocs.get_one_of_each()
    response = jsonify(documentation_one)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Enable CORS
    return response, 200

@app.route('/docs-two', methods=['GET'])
def get_documentation_two():
    """
    Endpoint: /docs-two
    Method:   GET
    Version:  v1
    Status:   Production
    Last Updated: 2024-08-17

    Description:
        Returns a JSON object containing two configurations from each category.
    """
    documentation_two = CacaoDocs.get_two_of_each()
    response = jsonify(documentation_two)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Enable CORS
    return response, 200

@app.route('/docs-four', methods=['GET'])
def get_documentation_four():
    """
    Endpoint: /docs-four
    Method:   GET
    Version:  v1
    Status:   Production
    Last Updated: 2025-01-02

    Description:
        Returns a JSON object containing four configurations from each category.
    """
    documentation_four = CacaoDocs.get_four_of_each()
    response = jsonify(documentation_four)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Enable CORS
    return response, 200

@app.route('/home')
def home():
    # Render the navbar.html template
    return render_template('navbar.html')

if __name__ == '__main__':
    app.run(debug=True)
