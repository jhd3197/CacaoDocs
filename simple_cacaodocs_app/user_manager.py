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
            @type{dict}: A dictionary containing the user's ID, username, and email.
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
