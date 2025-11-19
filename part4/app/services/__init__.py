from app.services.facade import HBnBFacade

facade = HBnBFacade()
"""
HBnBFacade instance acting as the main interface for the application.

This singleton-like object provides a unified API to interact with the
business logic layer, including operations on users, places, reviews,
and amenities.

Usage Example:
    # Creating a new user
    user_data = {
        "first_name": "Alice",
        "last_name": "Doe",
        "email": "alice@example.com"
    }
    new_user = facade.create_user(user_data)

    # Retrieving all places
    places = facade.get_all_places()

Attributes:
    facade (HBnBFacade): Instance providing access to all service operations.
"""
