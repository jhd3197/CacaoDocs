import unittest
from dataclasses import dataclass
from datetime import datetime

class TestTypes(unittest.TestCase):

    def test_parse_docstring_with_type_returns(self):
        from cacaodocs import CacaoDocs

        # Load the configuration for CacaoDocs
        CacaoDocs.load_config()

        # Define the Country dataclass with documentation
        @dataclass
        @CacaoDocs.doc_api(doc_type="types", tag="locations")
        class Country:
            """
            Last Updated: 2024-04-25
            Description:
                Represents a country in the system.

            Args:
                id (str): Unique identifier for the country
                code (str): The ISO country code (e.g., 'US', 'UK')
                name (str): The full country name
                phone_code (str): International dialing code
                created_at (datetime): Timestamp when the record was created
                updated_at (datetime): Timestamp when the record was last updated
            """
            id: str
            code: str
            name: str
            phone_code: str
            created_at: datetime
            updated_at: datetime

        # Define the City dataclass with documentation
        @dataclass
        @CacaoDocs.doc_api(doc_type="types", tag="locations")
        class City:
            """
            Last Updated: 2024-05-10
            Description:
                Represents a city in the system.

            Args:
                id (str): Unique identifier for the city
                name (str): The name of the city
                country_id (str): Reference to the associated country
                population (int): Population of the city
                created_at (datetime): Timestamp when the record was created
                updated_at (datetime): Timestamp when the record was last updated
            """
            id: str
            name: str
            country_id: str
            population: int
            created_at: datetime
            updated_at: datetime

        # Define the Language dataclass with documentation
        @dataclass
        @CacaoDocs.doc_api(doc_type="types", tag="languages")
        class Language:
            """
            Last Updated: 2024-06-15
            Description:
                Represents a language supported in the system.

            Args:
                id (str): Unique identifier for the language
                code (str): The ISO language code (e.g., 'en', 'es')
                name (str): The name of the language
                native_name (str): The native name of the language
                created_at (datetime): Timestamp when the record was created
                updated_at (datetime): Timestamp when the record was last updated
            """
            id: str
            code: str
            name: str
            native_name: str
            created_at: datetime
            updated_at: datetime

        # Define the Currency dataclass with documentation
        @dataclass
        @CacaoDocs.doc_api(doc_type="types", tag="financial")
        class Currency:
            """
            Last Updated: 2024-07-20
            Description:
                Represents a currency used in financial transactions.

            Args:
                id (str): Unique identifier for the currency
                code (str): The ISO currency code (e.g., 'USD', 'EUR')
                name (str): The name of the currency
                symbol (str): The symbol of the currency (e.g., '$', '€')
                created_at (datetime): Timestamp when the record was created
                updated_at (datetime): Timestamp when the record was last updated
            """
            id: str
            code: str
            name: str
            symbol: str
            created_at: datetime
            updated_at: datetime

        # Retrieve the generated documentation
        documentation = CacaoDocs.get_json()

        # Helper function to validate type documentation
        def validate_type(doc, expected):
            self.assertEqual(doc['function_name'], expected['function_name'])
            self.assertEqual(doc['tag'], expected['tag'])
            self.assertEqual(doc['type'], expected['type'])
            self.assertEqual(doc['last_updated'], expected['last_updated'])
            self.assertEqual(doc['description'], expected['description'])
            
            for arg_name, arg_props in expected['args'].items():
                self.assertIn(arg_name, doc['args'])
                self.assertEqual(doc['args'][arg_name]['type'], arg_props['type'])
                self.assertEqual(doc['args'][arg_name]['description'], arg_props['description'])
                self.assertEqual(doc['args'][arg_name]['emoji'], arg_props['emoji'])
                self.assertEqual(doc['args'][arg_name]['color'], arg_props['color'])
                self.assertEqual(doc['args'][arg_name]['bg_color'], arg_props['bg_color'])

        # Define expected documentation for Country
        expected_country = {
            'function_name': 'Country',
            'tag': 'locations',
            'type': 'types',
            'last_updated': '2024-04-25T00:00:00',
            'description': 'Represents a country in the system.',
            'args': {
                'id': {'type': 'str', 'description': 'Unique identifier for the country', 'emoji': '🔑', 'color': '#0EA5E9', 'bg_color': '#E0F2FE'},
                'code': {'type': 'str', 'description': "The ISO country code (e.g., 'US', 'UK')", 'emoji': '📝', 'color': '#22C55E', 'bg_color': '#DCFCE7'},
                'name': {'type': 'str', 'description': 'The full country name', 'emoji': '📝', 'color': '#22C55E', 'bg_color': '#DCFCE7'},
                'phone_code': {'type': 'str', 'description': 'International dialing code', 'emoji': '📝', 'color': '#22C55E', 'bg_color': '#DCFCE7'},
                'created_at': {'type': 'datetime', 'description': 'Timestamp when the record was created', 'emoji': '📅', 'color': '#d97d37', 'bg_color': '#F1F5F9'},
                'updated_at': {'type': 'datetime', 'description': 'Timestamp when the record was last updated', 'emoji': '📅', 'color': '#d97d37', 'bg_color': '#F1F5F9'}
            }
        }

        # Define expected documentation for City
        expected_city = {
            'function_name': 'City',
            'tag': 'locations',
            'type': 'types',
            'last_updated': '2024-05-10T00:00:00',
            'description': 'Represents a city in the system.',
            'args': {
                'id': {'type': 'str', 'description': 'Unique identifier for the city', 'emoji': '🔑', 'color': '#0EA5E9', 'bg_color': '#E0F2FE'},
                'name': {'type': 'str', 'description': 'The name of the city', 'emoji': '📝', 'color': '#22C55E', 'bg_color': '#DCFCE7'},
                'country_id': {'type': 'str', 'description': 'Reference to the associated country', 'emoji': '🔑', 'color': '#0EA5E9', 'bg_color': '#E0F2FE'},
                'population': {'type': 'int', 'description': 'Population of the city', 'emoji': '🔢', 'color': '#3B82F6', 'bg_color': '#DBEAFE'},
                'created_at': {'type': 'datetime', 'description': 'Timestamp when the record was created', 'emoji': '📅', 'color': '#d97d37', 'bg_color': '#F1F5F9'},
                'updated_at': {'type': 'datetime', 'description': 'Timestamp when the record was last updated', 'emoji': '📅', 'color': '#d97d37', 'bg_color': '#F1F5F9'}
            }
        }

        # Define expected documentation for Language
        expected_language = {
            'function_name': 'Language',
            'tag': 'languages',
            'type': 'types',
            'last_updated': '2024-06-15T00:00:00',
            'description': 'Represents a language supported in the system.',
            'args': {
                'id': {'type': 'str', 'description': 'Unique identifier for the language', 'emoji': '🔑', 'color': '#0EA5E9', 'bg_color': '#E0F2FE'},
                'code': {'type': 'str', 'description': "The ISO language code (e.g., 'en', 'es')", 'emoji': '📝', 'color': '#22C55E', 'bg_color': '#DCFCE7'},
                'name': {'type': 'str', 'description': 'The name of the language', 'emoji': '📝', 'color': '#22C55E', 'bg_color': '#DCFCE7'},
                'native_name': {'type': 'str', 'description': 'The native name of the language', 'emoji': '📝', 'color': '#22C55E', 'bg_color': '#DCFCE7'},
                'created_at': {'type': 'datetime', 'description': 'Timestamp when the record was created', 'emoji': '📅', 'color': '#d97d37', 'bg_color': '#F1F5F9'},
                'updated_at': {'type': 'datetime', 'description': 'Timestamp when the record was last updated', 'emoji': '📅', 'color': '#d97d37', 'bg_color': '#F1F5F9'}
            }
        }

        # Define expected documentation for Currency
        expected_currency = {
            'function_name': 'Currency',
            'tag': 'financial',
            'type': 'types',
            'last_updated': '2024-07-20T00:00:00',
            'description': 'Represents a currency used in financial transactions.',
            'args': {
                'id': {'type': 'str', 'description': 'Unique identifier for the currency', 'emoji': '🔑', 'color': '#0EA5E9', 'bg_color': '#E0F2FE'},
                'code': {'type': 'str', 'description': "The ISO currency code (e.g., 'USD', 'EUR')", 'emoji': '📝', 'color': '#22C55E', 'bg_color': '#DCFCE7'},
                'name': {'type': 'str', 'description': 'The name of the currency', 'emoji': '📝', 'color': '#22C55E', 'bg_color': '#DCFCE7'},
                'symbol': {'type': 'str', 'description': 'The symbol of the currency (e.g., \'$\', \'€\')', 'emoji': '📝', 'color': '#22C55E', 'bg_color': '#DCFCE7'},
                'created_at': {'type': 'datetime', 'description': 'Timestamp when the record was created', 'emoji': '📅', 'color': '#d97d37', 'bg_color': '#F1F5F9'},
                'updated_at': {'type': 'datetime', 'description': 'Timestamp when the record was last updated', 'emoji': '📅', 'color': '#d97d37', 'bg_color': '#F1F5F9'}
            }
        }

        # Map expected types for easy access
        expected_types = {
            'Country': expected_country,
            'City': expected_city,
            'Language': expected_language,
            'Currency': expected_currency
        }

        # Iterate through each type in the documentation and validate
        for doc in documentation['types']:
            func_name = doc['function_name']
            if func_name in expected_types:
                validate_type(doc, expected_types[func_name])

        # Additionally, ensure all expected types are present in the documentation
        documented_types = {doc['function_name'] for doc in documentation['types']}
        for expected in expected_types:
            self.assertIn(expected, documented_types, f"{expected} type is missing from documentation.")

# To run the tests, you can include the following block
if __name__ == '__main__':
    unittest.main()
