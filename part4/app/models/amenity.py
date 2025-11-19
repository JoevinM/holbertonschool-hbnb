from app.models.basemodel import BaseModel as BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship
from app import db

place_amenity = db.Table('place_amenity',
                         Column('place_id', Integer, ForeignKey(
                             'places.id'), primary_key=True),
                         Column('amenity_id', Integer, ForeignKey(
                             'amenities.id'), primary_key=True)
                         )


class Amenity(BaseModel):
    """Model representing an amenity (feature or service) available in a place.

    This class extends the BaseModel, inheriting common fields such as
    `id`, `created_at`, and `updated_at`.

    Attributes:
        name (str): The name of the amenity (e.g., "Wi-Fi", "Pool", "Parking").
    """
    __tablename__ = "amenities"
    name = db.Column(db.String(50), nullable=False)
    places = relationship('Place', secondary=place_amenity, lazy='subquery',
                          backref=db.backref('amenities', lazy=True))

    def __init__(self, name):
        """Initialize a new Amenity instance.

        Args:
            name (str): The name of the amenity.

        Raises:
            ValueError: If the name is empty or None.
        """
        super().__init__()
        self.name = name

    @validates('name')
    def verify_name(self, key, value):
        """Set the amenity's name.

        Args:
            value (str): The new name of the amenity.

        Raises:
            ValueError: If the name is empty or None.
        """
        if not value or len(value) > 50:
            raise ValueError
        return value
