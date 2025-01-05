from cacaodocs import CacaoDocs
import math

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

        Raises:
            KeyError: If the user with the specified ID does not exist.

        Returns:
            @type{dict}: A dictionary containing the user's ID, username, and email.
        """
        try:
            return self.users[user_id]
        except KeyError:
            raise KeyError(f"User with ID {user_id} does not exist.")

    @CacaoDocs.doc_api(doc_type="docs", tag="user_manager")
    def update_user(self, user_id: int, username: str = None, email: str = None) -> dict:
        """
        Method: update_user
        Version: v1
        Status: Production
        Last Updated: 2024-10-01

        Description:
            Updates the username and/or email of an existing user.

        Args:
            user_id (int): The unique identifier of the user.
            username (str, optional): The new username for the user.
            email (str, optional): The new email address for the user.

        Returns:
            @type{dict}: A dictionary containing the updated user's ID, username, and email.

        Raises:
            KeyError: If the user with the specified ID does not exist.
            ValueError: If neither username nor email is provided for update.
        """
        if user_id not in self.users:
            raise KeyError(f"User with ID {user_id} does not exist.")

        if not username and not email:
            raise ValueError("At least one of 'username' or 'email' must be provided for update.")

        if username:
            self.users[user_id]["username"] = username
        if email:
            self.users[user_id]["email"] = email

        return self.users[user_id]

    @CacaoDocs.doc_api(doc_type="docs", tag="user_manager")
    def delete_user(self, user_id: int) -> str:
        """
        Method: delete_user
        Version: v1
        Status: Production
        Last Updated: 2024-10-12

        Description:
            Deletes a user from the database by their unique ID.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            @type{str}: A confirmation message indicating successful deletion.

        Raises:
            KeyError: If the user with the specified ID does not exist.
        """
        if user_id in self.users:
            del self.users[user_id]
            return f"User with ID {user_id} has been deleted."
        else:
            raise KeyError(f"User with ID {user_id} does not exist.")

    @CacaoDocs.doc_api(doc_type="docs", tag="user_manager")
    def list_users(self) -> list:
        """
        Method: list_users
        Version: v1
        Status: Production
        Last Updated: 2024-10-14

        Description:
            Retrieves a list of all users in the database.

        Returns:
            @type{list}: A list of dictionaries, each containing a user's ID, username, and email.
        """
        return list(self.users.values())
    
class Calculator:
    @CacaoDocs.doc_api(doc_type="docs", tag="calculator")
    def add(self, a, b):
        """
        Method: add
        Version: v1
        Status: Production
        Last Updated: 2024-11-12
        
        Description:
            Adds two numbers together.
            
        Args:
            a (float): First number
            b (float): Second number
            
        Returns:
            @type{float}: The sum of a and b
        """
        return a + b

    @CacaoDocs.doc_api(doc_type="docs", tag="calculator")
    def subtract(self, a, b):
        """
        Method: subtract
        Version: v1
        Status: Production
        Last Updated: 2024-11-11
        
        Description:
            Subtracts second number from first number.
            
        Args:
            a (float): First number
            b (float): Second number
            
        Returns:
            @type{float}: The difference between a and b
        """
        return a - b

    @CacaoDocs.doc_api(doc_type="docs", tag="calculator")
    def multiply(self, a: float, b: float) -> float:
        """
        Method: multiply
        Version: v1
        Status: Production
        Last Updated: 2024-02-12
        
        Description:
            multiply two numbers together.
            
        Args:
            a (float): First number
            b (float): Second number
            
        Returns:
            @type{float}: The difference between a and b
        """
        return a * b

    def divide(self, a, b):
        """
        Method: divide
        Version: v1
        Status: Production
        Last Updated: 2024-02-12
        
        Description:
            Divides first number by second number.
            
        Args:
            a (float): First number
            b (float): Second number
            
        Returns:
            float: The result of a divided by b
            
        Raises:
            ValueError: If attempting to divide by zero
        """
        if b != 0:
            return a / b
        else:
            raise ValueError("Cannot divide by zero")

    @CacaoDocs.doc_api(doc_type="docs", tag="calculator")
    def calculator_status_check(self) -> str:
        """
        Method: calculator_status_check
        Version: v1
        Status: Production

        Description:
            Check if the calculator is operational.

        Returns:
            @type{str}: The operational status of the calculator
        """
        return "Calculator is operational", 200
    

class ScientificCalculator:
    @CacaoDocs.doc_api(doc_type="docs", tag="scientific_calculator")
    def power(self, base: float, exponent: float) -> float:
        """
        Method: power
        Version: v1
        Status: Production
        Last Updated: 2024-02-12
        
        Description:
            Raises a base number to the power of an exponent.
            
        Args:
            base (float): The base number.
            exponent (float): The exponent to raise the base to.
            
        Returns:
            @type{float}: The result of base raised to the power of exponent.
        """
        return math.pow(base, exponent)

    @CacaoDocs.doc_api(doc_type="docs", tag="scientific_calculator")
    def sqrt(self, number: float) -> float:
        """
        Method: sqrt
        Version: v1
        Status: Production
        Last Updated: 2024-02-12
        
        Description:
            Calculates the square root of a number.
            
        Args:
            number (float): The number to find the square root of.
            
        Returns:
            @type{float}: The square root of the number.
        """
        if number < 0:
            raise ValueError("Cannot calculate square root of a negative number.")
        return math.sqrt(number)

    @CacaoDocs.doc_api(doc_type="docs", tag="scientific_calculator")
    def logarithm(self, number: float, base: float = math.e) -> float:
        """
        Method: logarithm
        Version: v1
        Status: Production
        Last Updated: 2024-02-12
        
        Description:
            Calculates the logarithm of a number with a specified base.
            
        Args:
            number (float): The number to calculate the logarithm for.
            base (float, optional): The base of the logarithm. Defaults to e.
            
        Returns:
            @type{float}: The logarithm of the number with the specified base.
        """
        if number <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers.")
        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be positive and not equal to 1.")
        return math.log(number, base)

    @CacaoDocs.doc_api(doc_type="docs", tag="scientific_calculator")
    def sine(self, angle_degrees: float) -> float:
        """
        Method: sine
        Version: v1
        Status: Production
        Last Updated: 2024-02-12
        
        Description:
            Calculates the sine of an angle provided in degrees.
            
        Args:
            angle_degrees (float): The angle in degrees.
            
        Returns:
            @type{float}: The sine of the angle.
        """
        angle_radians = math.radians(angle_degrees)
        return math.sin(angle_radians)

    @CacaoDocs.doc_api(doc_type="docs", tag="scientific_calculator")
    def cosine(self, angle_degrees: float) -> float:
        """
        Method: cosine
        Version: v1
        Status: Production
        Last Updated: 2024-02-12
        
        Description:
            Calculates the cosine of an angle provided in degrees.
            
        Args:
            angle_degrees (float): The angle in degrees.
            
        Returns:
            @type{float}: The cosine of the angle.
        """
        angle_radians = math.radians(angle_degrees)
        return math.cos(angle_radians)

    @CacaoDocs.doc_api(doc_type="docs", tag="scientific_calculator")
    def tangent(self, angle_degrees: float) -> float:
        """
        Method: tangent
        Version: v1
        Status: Production
        Last Updated: 2024-02-12
        
        Description:
            Calculates the tangent of an angle provided in degrees.
            
        Args:
            angle_degrees (float): The angle in degrees.
            
        Returns:
            @type{float}: The tangent of the angle.
        """
        angle_radians = math.radians(angle_degrees)
        cosine = math.cos(angle_radians)
        if cosine == 0:
            raise ValueError("Tangent undefined for angles where cosine is zero.")
        return math.tan(angle_radians)
