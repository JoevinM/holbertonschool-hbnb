from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """Base model providing common attributes and methods for all entities.

    Attributes:
        id (str): Unique identifier for the object (UUID4).
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of the last modification.
    """
    __abstract__ = True
    # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Update the `updated_at` timestamp to the current time."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update object attributes based on a provided dictionary.

        Args:
            data (dict): A dictionary of attribute names and new values.

        Notes:
            - Only existing public attributes are updated.
            - Automatically updates the `updated_at` timestamp.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
