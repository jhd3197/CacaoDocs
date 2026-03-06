"""Sample FastAPI application for testing CacaoDocs doc types."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}")
def get_user(user_id: int, include: str = None):
    """Get a user by their ID.

    Type: api

    Method: GET
    Path: /users/{user_id}

    Path Params:
        user_id (int): The user's unique identifier.

    Query Params:
        include (str): Comma-separated list of fields to include.

    Response (200):
        id (int): The user ID.
        name (str): The user's full name.
        email (str): The user's email address.

    Response (404):
        detail (str): User not found error message.

    Examples:
        >>> GET /users/42
        {"id": 42, "name": "Alice", "email": "alice@example.com"}
    """
    return {"id": user_id, "name": "Alice", "include": include}


@app.post("/users")
async def create_user(name: str, email: str):
    """Create a new user account.

    Type: api

    Method: POST
    Path: /users

    Request Body:
        name (str, required): The user's full name.
        email (str, required): The user's email address.

    Response (201):
        id (int): The newly created user ID.
        name (str): The user's name.

    Response (400):
        detail (str): Validation error message.
    """
    return {"id": 1, "name": name, "email": email}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Delete a user permanently.

    Type: api

    Method: DELETE
    Path: /users/{user_id}

    Path Params:
        user_id (int): The user to delete.

    Response (204):

    Response (404):
        detail (str): User not found.
    """
    return {"deleted": user_id}
