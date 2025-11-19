from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.services.repositories.user_repository import UserRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.services.repositories.review_repository import ReviewRepository


class HBnBFacade:
    """Facade providing a unified interface to manage Users, Places,
    Amenities, and Reviews using in-memory repositories.

    This class encapsulates the business logic layer and centralizes
    access to all CRUD operations on the core entities.
    """

    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    """USER"""

    def create_user(self, user_data):
        """Create a new user and store it in the repository.

        Args:
            user_data (dict): Dictionary containing user attributes.

        Returns:
            User: The created user instance.
        """
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email address."""
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
        """Update a user by ID."""
        self.user_repo.update(user_id, update_data)

    """"AMENITY"""

    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """Retrieve an amenity by its name."""
        return self.amenity_repo.get_amenity_by_name(name)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity by ID."""
        self.amenity_repo.update(amenity_id, amenity_data)

    """PLACE"""

    def create_place(self, place_data):
        """Create a new place."""
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        return self.place_repo.get(place_id)

    def get_place_by_localisation(self, place_lat, place_long):
        """Check if a place exists at given latitude and longitude.

        Returns:
            bool: True if a place exists at the coordinates, False otherwise.
        """
        latitude = self.place_repo.get_by_attribute('latitude', place_lat)
        longitude = self.place_repo.get_by_attribute('longitude', place_long)
        if latitude is None or longitude is None:
            return False
        else:
            return True

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place by ID."""
        self.place_repo.update(place_id, place_data)

    """REVIEW"""

    def create_review(self, review_data):
        """Create a new review."""
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve the first review for a given place ID."""
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        """Update a review by ID."""
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review by ID."""
        self.review_repo.delete(review_id)
