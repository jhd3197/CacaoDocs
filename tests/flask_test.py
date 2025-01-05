# test_api_endpoints.py

import unittest
from dataclasses import dataclass
from datetime import datetime
from flask import Flask, jsonify, request
from cacaodocs import CacaoDocs

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        # Initialize CacaoDocs configuration
        CacaoDocs.load_config()

        # Create a Flask app instance for testing
        self.app = Flask(__name__)

        # Define Flask endpoints with CacaoDocs decorators
        self.define_endpoints()

    def define_endpoints(self):
        # Define the delete_user endpoint
        @self.app.route('/api/users/<int:user_id>', methods=['DELETE'])
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
                404:
                    example: {"error": "User not found."}
            """
            try:
                # Simulate deletion logic
                # db.delete_user(user_id)
                return jsonify({"message": f"User {user_id} deleted successfully."}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 404

        # Define the list_users endpoint
        @self.app.route('/api/users', methods=['GET'])
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
                    description:List of users retrieved successfully.
                    example: [{"id": 12345,"username": "johndoe"}]
                304:
                    description:No users found in the system.
                    example: {"message": "No users found."}
            """
            # Simulate retrieval logic
            # users = db.list_users()
            users = [{"id": 12345, "username": "johndoe"}]  # Example data
            if users:
                return jsonify(users), 200
            else:
                return jsonify({"message": "No users found."}), 304

        # Define the create_user endpoint
        @self.app.route('/api/users', methods=['POST'])
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
                data (dict): The user data payload.

            Responses:
                201:
                    description:User successfully created.
                    example: {"id": 12345,"username": "johndoe"}
                400:
                    description:Bad request due to invalid input.
                    example: {"error": "Invalid email format."}
            """
            data = request.json or {}
            try:
                # Simulate user creation logic
                # user = db.create_user(data)
                user = {"id": 12345, "username": "johndoe"}  # Example data
                return jsonify(user), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 400

        # Define additional endpoints as needed...

    def test_parse_docstring_with_api_returns(self):
        # Retrieve the generated documentation
        documentation = CacaoDocs.get_json()

        # Helper function to validate API documentation
        def validate_api(doc, expected):
            with self.subTest(function_name=expected['function_name']):
                self.assertEqual(doc['function_name'], expected['function_name'],
                                 f"Function name mismatch for {expected['function_name']}. Expected '{expected['function_name']}', got '{doc['function_name']}'")
                self.assertEqual(doc['tag'], expected['tag'],
                                 f"Tag mismatch for {expected['function_name']}'. Expected '{expected['tag']}', got '{doc['tag']}'")
                self.assertEqual(doc['type'], expected['type'],
                                 f"Type mismatch for {expected['function_name']}'. Expected '{expected['type']}', got '{doc['type']}'")
                self.assertEqual(doc['last_updated'], expected['last_updated'],
                                 f"Last updated mismatch for {expected['function_name']}'. Expected '{expected['last_updated']}', got '{doc['last_updated']}'")
                self.assertEqual(doc['description'], expected['description'],
                                 f"Description mismatch for {expected['function_name']}'. Expected '{expected['description']}', got '{doc['description']}'")
                self.assertEqual(doc['method'], expected['method'],
                                 f"HTTP method mismatch for {expected['function_name']}'. Expected '{expected['method']}', got '{doc['method']}'")
                self.assertEqual(doc['endpoint'], expected['endpoint'],
                                 f"Endpoint mismatch for {expected['function_name']}'. Expected '{expected['endpoint']}', got '{doc['endpoint']}'")
                self.assertEqual(doc['version'], expected['version'],
                                 f"Version mismatch for {expected['function_name']}'. Expected '{expected['version']}', got '{doc['version']}'")
                self.assertEqual(doc['status'], expected['status'],
                                 f"Status mismatch for {expected['function_name']}'. Expected '{expected['status']}', got '{doc['status']}'")

                # Validate Args
                for arg_name, arg_props in expected.get('args', {}).items():
                    with self.subTest(function_name=expected['function_name'], arg_name=arg_name):
                        self.assertIn(arg_name, doc.get('args', {}),
                                      f"Argument '{arg_name}' missing in documentation for '{expected['function_name']}'")
                        actual_arg = doc['args'][arg_name]
                        expected_arg = arg_props
                        self.assertEqual(actual_arg['type'], expected_arg['type'],
                                         f"Type mismatch for argument '{arg_name}' in '{expected['function_name']}'. Expected '{expected_arg['type']}', got '{actual_arg['type']}'")
                        self.assertEqual(actual_arg['description'], expected_arg['description'],
                                         f"Description mismatch for argument '{arg_name}' in '{expected['function_name']}'. Expected '{expected_arg['description']}', got '{actual_arg['description']}'")
                        self.assertEqual(actual_arg['emoji'], expected_arg['emoji'],
                                         f"Emoji mismatch for argument '{arg_name}' in '{expected['function_name']}'. Expected '{expected_arg['emoji']}', got '{actual_arg['emoji']}'")
                        self.assertEqual(actual_arg['color'], expected_arg['color'],
                                         f"Color mismatch for argument '{arg_name}' in '{expected['function_name']}'. Expected '{expected_arg['color']}', got '{actual_arg['color']}'")
                        self.assertEqual(actual_arg['bg_color'], expected_arg['bg_color'],
                                         f"Background color mismatch for argument '{arg_name}' in '{expected['function_name']}'. Expected '{expected_arg['bg_color']}', got '{actual_arg['bg_color']}'")

                # Validate Responses
                for status_code, response_props in expected.get('responses', {}).items():
                    with self.subTest(function_name=expected['function_name'], response=status_code):
                        self.assertIn(status_code, doc.get('responses', {}),
                                      f"Response '{status_code}' missing in documentation for '{expected['function_name']}'")
                        actual_response = doc['responses'][status_code]
                        expected_response = response_props
                        self.assertEqual(actual_response.get('description'), expected_response.get('description'),
                                         f"Description mismatch for response '{status_code}' in '{expected['function_name']}'. Expected '{expected_response.get('description')}', got '{actual_response.get('description')}'")
                        self.assertEqual(actual_response.get('example'), expected_response.get('example'),
                                         f"Example mismatch for response '{status_code}' in '{expected['function_name']}'. Expected '{expected_response.get('example')}', got '{actual_response.get('example')}'")

        # Define expected documentation for each API endpoint
        expected_create_user = {
            'function_name': 'create_user',
            'tag': 'users',
            'type': 'api',
            'last_updated': '2024-04-25T00:00:00',
            'description': 'Creates a new user with the provided details.',
            'method': 'POST',
            'endpoint': '/api/users',
            'version': 'v1',
            'status': 'Production',
            'responses': {
                '201': {
                    'description': "User successfully created.",
                    'example': '{"id": 12345,"username": "johndoe"}'
                },
                '400': {
                    'description': "Bad request due to invalid input.",
                    'example': '{"error": "Invalid email format."}'
                }
            }
        }

        expected_delete_user = {
            'function_name': 'delete_user',
            'tag': 'users',
            'type': 'api',
            'last_updated': '2024-04-24T00:00:00',
            'description': 'Deletes an existing user from the system.',
            'method': 'DELETE',
            'endpoint': '/api/users/<user_id>',
            'version': 'v1',
            'status': 'In Review',
            'args': {
                'user_id': {
                    'type': 'int',
                    'description': 'The unique identifier of the user.',
                    'emoji': '🔑',
                    'color': '#0EA5E9',
                    'bg_color': '#E0F2FE'
                }
            },
            'responses': {
                '200': {
                    'example': '{"message": "User 12345 deleted successfully."}'
                },
                '404': {
                    'example': '{"error": "User not found."}'
                }
            }
        }

        expected_list_users = {
            'function_name': 'list_users',
            'tag': 'users',
            'type': 'api',
            'last_updated': '2025-01-02T00:00:00',
            'description': 'Retrieves a list of all users in the system.',
            'method': 'GET',
            'endpoint': '/api/users',
            'version': 'v1',
            'status': 'Planned',
            'responses': {
                '200': {
                    'description': "List of users retrieved successfully.",
                    'example': '[{"id": 12345,"username": "johndoe"}]'
                },
                '304': {
                    'description': "No users found in the system.",
                    'example': '{"message": "No users found."}'
                }
            }
        }

        # Map expected APIs for easy access
        expected_apis = {
            'create_user': expected_create_user,
            'delete_user': expected_delete_user,
            'list_users': expected_list_users,
            # Add more expected APIs here...
        }

        # Iterate through each API in the documentation and validate
        for doc in documentation.get('api', []):
            func_name = doc.get('function_name')
            if func_name in expected_apis:
                validate_api(doc, expected_apis[func_name])

        # Additionally, ensure all expected APIs are present in the documentation
        documented_apis = {doc.get('function_name') for doc in documentation.get('api', [])}
        for expected in expected_apis:
            self.assertIn(expected, documented_apis, f"{expected} API endpoint is missing from documentation.")

# To run the tests, include the following block
if __name__ == '__main__':
    unittest.main(verbosity=2)
