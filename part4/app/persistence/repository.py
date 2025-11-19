from abc import ABC, abstractmethod
from app import db


class Repository(ABC):
    """Abstract base class defining the interface for a repository.

    This repository pattern can be implemented for any storage type
    (e.g., in-memory, database) for managing entities.
    """

    @abstractmethod
    def add(self, obj):
        """Add a new object to the repository.

        Args:
            obj: The object to add.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID.

        Args:
            obj_id (str): Unique identifier of the object.

        Returns:
            The object if found, else None.
        """
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects from the repository.

        Returns:
            List of all objects.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object by its ID.

        Args:
            obj_id (str): Unique identifier of the object.
            data (dict): Dictionary of attributes to update.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by its ID.

        Args:
            obj_id (str): Unique identifier of the object to delete.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute value.

        Args:
            attr_name (str): Name of the attribute.
            attr_value: Value of the attribute to match.

        Returns:
            The first object matching the attribute, or None if not found.
        """
        pass


class InMemoryRepository(Repository):
    """In-memory implementation of the Repository interface.

    Stores objects in a dictionary keyed by their `id` attribute.
    """

    def __init__(self):
        """Initialize the in-memory storage."""
        self._storage = {}

    def add(self, obj):
        """Add an object to the repository."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object by its ID."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Retrieve all stored objects."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object with the given data if it exists."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Remove an object from the repository by its ID."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve the first object with a matching attribute value."""
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name, None) == attr_value),
            None
        )


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
