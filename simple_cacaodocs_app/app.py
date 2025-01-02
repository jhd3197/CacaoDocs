from flask import Flask, request, jsonify
from cacaodocs import CacaoDocs
from user_manager import UserManager

# Initialize CacaoDocs
CacaoDocs.load_config()

app = Flask(__name__)

# Initialize UserManager
db = UserManager()

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
            example: {"id": 1, "username": "johndoe", "email": "johndoe@example.com"}
        400:
            description: "Bad request due to invalid input."
            example: {"error": "Invalid email format."}
    """
    data = request.json or {}
    username = data.get('username')
    email = data.get('email')
    if not username or not email:
        return jsonify({"error": "Username and email are required."}), 400
    try:
        user = db.create_user(username, email)
        return jsonify(user), 201
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

    Raises:
        KeyError: If no user is found with the given `user_id`.

    Responses:
        200:
            description: "User data retrieved successfully."
            example: {"id": 1, "username": "johndoe", "email": "johndoe@example.com"}
        404:
            description: "User not found."
            example: {"error": "User with ID 999 does not exist."}
    """
    try:
        user = db.get_user(user_id)
        return jsonify(user), 200
    except KeyError as e:
        return jsonify({"error": str(e)}), 404

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

if __name__ == '__main__':
    app.run(debug=True)
