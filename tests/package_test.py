# test_package.py

import unittest
from cacaodocs import CacaoDocs

class TestPackage(unittest.TestCase):

    def test_parse_docstring_with_package_returns(self):
        # Load the configuration for CacaoDocs
        CacaoDocs.load_config()

        # Define the UserManager class with CacaoDocs decorators and docstrings
        class UserManager:
            def __init__(self):
                self.users = {}
                self.next_id = 1

            @CacaoDocs.doc_api(doc_type="docs", tag="user_manager")
            def create_user(self, username: str, email: str) -> dict:
                """
                Method: create_user
                Version: v1
                Status: Production
                Last Updated: 2024-02-12

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
                Last Updated: 2025-01-01

                Description:
                    Retrieves the details of a user by their unique ID.

                Args:
                    user_id (int): The unique identifier of the user.

                Returns:
                    @type{dict}: A dictionary containing the user's ID, username, and email.
                """
                try:
                    return self.users[user_id]
                except KeyError:
                    raise KeyError(f"User with ID {user_id} does not exist.")

        # Instantiate UserManager to ensure methods are processed
        user_manager = UserManager()

        # Optionally, call methods to simulate usage (not strictly necessary for documentation)
        user_manager.create_user("johndoe", "johndoe@example.com")
        try:
            user_manager.get_user(99999)  # This will raise KeyError
        except KeyError:
            pass  # Expected exception

        # Retrieve the generated documentation
        documentation = CacaoDocs.get_json()

        # Helper function to validate documentation entries
        def validate_doc(doc, expected):
            with self.subTest(function_name=expected['function_name']):
                # Validate top-level fields
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
                                 f"Method mismatch for {expected['function_name']}'. Expected '{expected['method']}', got '{doc['method']}'")

                # Validate Args
                expected_args = expected.get('args', {})
                for arg_name, arg_props in expected_args.items():
                    with self.subTest(function_name=expected['function_name'], arg_name=arg_name):
                        self.assertIn(arg_name, doc.get('args', {}),
                                      f"Argument '{arg_name}' missing in documentation for '{expected['function_name']}'")
                        actual_arg = doc['args'][arg_name]
                        self.assertEqual(actual_arg['type'], arg_props['type'],
                                         f"Type mismatch for argument '{arg_name}' in '{expected['function_name']}'. Expected '{arg_props['type']}', got '{actual_arg['type']}'")
                        self.assertEqual(actual_arg['description'], arg_props['description'],
                                         f"Description mismatch for argument '{arg_name}' in '{expected['function_name']}'. Expected '{arg_props['description']}', got '{actual_arg['description']}'")
                        self.assertEqual(actual_arg['emoji'], arg_props['emoji'],
                                         f"Emoji mismatch for argument '{arg_name}' in '{expected['function_name']}'. Expected '{arg_props['emoji']}', got '{actual_arg['emoji']}'")
                        self.assertEqual(actual_arg['color'], arg_props['color'],
                                         f"Color mismatch for argument '{arg_name}' in '{expected['function_name']}'. Expected '{arg_props['color']}', got '{actual_arg['color']}'")
                        self.assertEqual(actual_arg['bg_color'], arg_props['bg_color'],
                                         f"Background color mismatch for argument '{arg_name}' in '{expected['function_name']}'. Expected '{arg_props['bg_color']}', got '{actual_arg['bg_color']}'")

                # Validate Returns
                expected_returns = expected.get('returns')
                if expected_returns:
                    self.assertEqual(doc.get('returns'), expected_returns,
                                     f"Returns mismatch for '{expected['function_name']}'. Expected '{expected_returns}', got '{doc.get('returns')}'")

        # Define expected documentation for create_user
        expected_create_user = {
            'function_name': 'create_user',
            'tag': 'user_manager',
            'type': 'docs',
            'last_updated': '2024-02-12T00:00:00',
            'description': 'Creates a new user with a unique ID, username, and email.',
            'method': 'create_user',
            'args': {
                'username': {
                    'type': 'str',
                    'description': 'The username of the new user.',
                    'emoji': '📝',
                    'color': '#22C55E',
                    'bg_color': '#DCFCE7'
                },
                'email': {
                    'type': 'str',
                    'description': 'The email address of the new user.',
                    'emoji': '📧',
                    'color': '#02a6ed',
                    'bg_color': '#FEE2E2'
                }
            },
            'returns': '@type{User}'
        }

        # Define expected documentation for get_user
        expected_get_user = {
            'function_name': 'get_user',
            'tag': 'user_manager',
            'type': 'docs',
            'last_updated': '2025-01-01T00:00:00',
            'description': 'Retrieves the details of a user by their unique ID.',
            'method': 'get_user',
            'args': {
                'user_id': {
                    'type': 'int',
                    'description': 'The unique identifier of the user.',
                    'emoji': '🔑',
                    'color': '#0EA5E9',
                    'bg_color': '#E0F2FE'
                }
            },
            'returns': {
                'description': "A dictionary containing the user's ID, username, and email.",
                'full_type': 'dict',
                'is_list': False,
                'is_type_ref': True,
                'type_name': 'dict'
            }
        }

        # Map expected documentation for easy access
        expected_docs = {
            'create_user': expected_create_user,
            'get_user': expected_get_user
        }

        # Iterate through each documentation entry and validate
        for doc in documentation.get('docs', []):
            func_name = doc.get('function_name')
            if func_name in expected_docs:
                validate_doc(doc, expected_docs[func_name])

        # Additionally, ensure all expected documentation entries are present
        documented_functions = {doc.get('function_name') for doc in documentation.get('docs', [])}
        for expected in expected_docs:
            self.assertIn(expected, documented_functions,
                          f"Documentation for '{expected}' is missing.")

# To run the tests, include the following block
if __name__ == '__main__':
    unittest.main(verbosity=2)
