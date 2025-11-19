from app.models.basemodel import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship
from app import db


class Place(BaseModel):
    """Model representing a place or property.

    Inherits from BaseModel and adds location, pricing, ownership,
    reviews, and amenities attributes.

    Attributes:
        title (str): Title of the place.
        description (str): Description of the place.
        price (float): Price per night (must be positive).
        latitude (float): Latitude coordinate (-90 to 90).
        longitude (float): Longitude coordinate (-180 to 180).
        owner_id (str): ID of the user who owns the place.
        reviews (list): List of reviews associated with the place.
        amenities (list): List of amenities associated with the place.
    """
    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviews = relationship('Review', backref='place',
                           lazy=True, cascade=('all, delete'))

    def __init__(self, title, description, price, latitude, longitude,
                 user, amenities=None):
        """Initialize a new Place instance with validation."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.user = user
        if amenities:
            self.amenities = amenities

    @validates("title")
    def verify_title(self, key, value):
        """Set the title of the place.

        Args:
            value (str): The new title.

        Raises:
            ValueError: If the title is empty or None.
        """
        if not value or type(value) is not str:
            raise ValueError
        return value

    @validates("price")
    def verify_price(self, key, value):
        """Set the price of the place.

        Args:
            value (float): The price per night.

        Raises:
            TypeError: If value is not a float.
            ValueError: If value is negative.
        """
        if type(value) is not float:
            raise TypeError("Price enter is not of type float")
        elif value < 0:
            raise ValueError("Price should be positive")
        return value

    @validates("latitude")
    def verify_latitude(self, key, value):
        """Set the latitude coordinate.

        Args:
            value (float): Latitude in degrees.

        Raises:
            TypeError: If value is not a float.
            ValueError: If value is not between -90 and 90.
        """
        if type(value) is not float:
            raise TypeError("Latitude must be a number")
        elif value > 90 or value < -90:
            raise ValueError("Latitude must be between 90 and -90")
        return value

    @validates("longitude")
    def verify_longitude(self, key, value):
        """Set the longitude coordinate.

        Args:
            value (float): Longitude in degrees.

        Raises:
            TypeError: If value is not a float.
            ValueError: If value is not between -180 and 180.
        """
        if type(value) is not float:
            raise TypeError("Longitude must be a number")
        elif value > 180 or value < -180:
            raise ValueError("Longitude must be between 180 and -180")
        return value
