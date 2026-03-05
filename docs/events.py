"""Application event handlers."""


def on_user_signup(user_data: dict):
    """Fires when a new user completes registration.

    Type: event

    Trigger: When a user submits the signup form and passes validation.

    Payload:
        user_id (int): The newly created user ID.
        email (str): The user's email address.
        plan (str): Selected subscription plan.

    Examples:
        >>> {"user_id": 42, "email": "new@user.com", "plan": "pro"}
    """
    pass


def on_payment_received(payment_data: dict):
    """Fires when a payment is successfully processed.

    Type: event

    Trigger: After Stripe webhook confirms payment_intent.succeeded.

    Payload:
        payment_id (str): Stripe payment intent ID.
        amount (int): Amount in cents.
        currency (str): Three-letter currency code.
        user_id (int): The paying user's ID.
    """
    pass
