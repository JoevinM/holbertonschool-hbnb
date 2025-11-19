from app.models.basemodel import BaseModel as BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates
from app import db


class Review(BaseModel):

    __tablename__ = 'reviews'

    """Model representing a review made by a user for a place.

    Inherits from BaseModel and adds attributes for the review text,
    rating, associated user, and associated place.

    Attributes:
        text (str): The textual content of the review.
        rating (int): Rating given to the place (1–5).
        user_id (str): ID of the user who made the review.
        place_id (str): ID of the place being reviewed.
    """
    text = db.Column(db.String(500))
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey(
        'places.id'), nullable=False)

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place

    @validates("text")
    def verify_text(self, key, value):
        """Verify the text of the review.

        Args:
            value (str): The textual content.

        Raises:
            ValueError: If the text is empty or None.
        """
        if not value or type(value) is not str or len(value) > 500:
            raise ValueError
        return value

    @validates("rating")
    def verify_rating(self, key, value):
        """Set the rating of the review with validation.

        Args:
            value (int): The rating value to assign
                (must be an integer between 1 and 5).

        Raises:
            ValueError: If the value is not an integer or not in the range 1-5.
        """
        if not value or not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value
