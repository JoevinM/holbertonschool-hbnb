import unittest
from app import create_app
from app.models.place import Place
from app.models.user import User
from app.services import facade


class TestUserEndpoints(unittest.TestCase):
    """Unit tests for Place API endpoints."""

    def setUp(self):
        """Set up the test client before each test."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place(self):
        """Test creating a new place with valid data returns 201."""
        owner_data = {"first_name": "Jean", "last_name": "Bon",
                      "email": "beurre@gmail.com"}
        owner = facade.create_user(owner_data)
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner.id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_empty_title(self):
        """Test creating a place with an empty title raises ValueError."""
        owner_data = {"first_name": "Jean", "last_name": "Bon",
                      "email": "beurre@gmail.com"}
        owner = facade.create_user(owner_data)
        self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner.id
        })
        self.assertRaises(ValueError)

    def test_create_invalid_price(self):
        """Test creating a place with negative price raises ValueError."""
        owner_data = {"first_name": "Jean", "last_name": "Bon",
                      "email": "beurre@gmail.com"}
        owner = facade.create_user(owner_data)
        self.client.post('/api/v1/places/', json={
            "title": "Cosy place",
            "description": "A nice place to stay",
            "price": -90,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner.id
        })
        self.assertRaises(ValueError)

    def test_create_invalid_type_price(self):
        """Test creating a place with non-float price raises TypeError."""
        owner_data = {"first_name": "Jean", "last_name": "Bon",
                      "email": "beurre@gmail.com"}
        owner = facade.create_user(owner_data)
        self.client.post('/api/v1/places/', json={
            "title": "Cosy place",
            "description": "A nice place to stay",
            "price": "yo",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner.id
        })
        self.assertRaises(TypeError)

    def test_create_invalid_latitude(self):
        """Test creating a place with latitude out of bounds
            raises ValueError."""
        owner_data = {"first_name": "Jean", "last_name": "Bon",
                      "email": "beurre@gmail.com"}
        owner = facade.create_user(owner_data)
        self.client.post('/api/v1/places/', json={
            "title": "Cosy place",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": -100.7749,
            "longitude": -122.4194,
            "owner_id": owner.id
        })
        self.assertRaises(ValueError)

    def test_create_invalid_type_latitude(self):
        """Test creating a place with non-float latitude raises TypeError."""
        owner_data = {"first_name": "Jean", "last_name": "Bon",
                      "email": "beurre@gmail.com"}
        owner = facade.create_user(owner_data)
        self.client.post('/api/v1/places/', json={
            "title": "Cosy place",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": "ah",
            "longitude": -122.4194,
            "owner_id": owner.id
        })
        self.assertRaises(TypeError)

    def test_create_invalid_longitude(self):
        """Test creating a place with longitude out of bounds
            raises ValueError."""
        owner_data = {"first_name": "Jean", "last_name": "Bon",
                      "email": "beurre@gmail.com"}
        owner = facade.create_user(owner_data)
        self.client.post('/api/v1/places/', json={
            "title": "Cosy place",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": -100.7749,
            "longitude": -222.4194,
            "owner_id": owner.id
        })
        self.assertRaises(ValueError)

    def test_create_invalid_type_longitude(self):
        """Test creating a place with non-float longitude raises TypeError."""
        owner_data = {"first_name": "Jean", "last_name": "Bon",
                      "email": "beurre@gmail.com"}
        owner = facade.create_user(owner_data)
        self.client.post('/api/v1/places/', json={
            "title": "Cosy place",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": -30.0,
            "longitude": -122,
            "owner_id": owner.id
        })
        self.assertRaises(TypeError)

    def test_create_empty_owner_id(self):
        """Test creating a place with empty owner_id raises ValueError."""
        self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": ""
        })
        self.assertRaises(ValueError)

    def test_create_place_invalid_owner_id(self):
        """Test creating a place with non-existing owner_id returns 400."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "aaaaaaah"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_same_place(self):
        """Test creating a duplicate place returns 400."""
        owner = User("Jean", "Bon", "beurre@gmail.com")
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner.id
        })
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner.id
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        """Test retrieving all places returns status 200."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_valid_update_place(self):
        """Test updating a place with valid data updates
            attributes correctly."""
        owner_data = {"first_name": "Jean", "last_name": "Bon",
                      "email": "beurre@gmail.com"}
        owner = facade.create_user(owner_data)
        new_place = Place("Cozy place", "noice", 100.0, 37.7, -122.4, owner.id)
        new_place.update({
            "title": "Cozy place",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7,
            "longitude": -122.4,
            "owner_id": owner.id})
        self.assertEqual(new_place.description, "A nice place to stay")

    def test_invalid_update_place(self):
        """Test updating a place with invalid title raises ValueError."""
        owner = User("Jean", "Bon", "beurre@gmail.com")
        new_place = Place("Cozy place", "noice", 100.0, 37.7, -122.4, owner.id)
        with self.assertRaises(ValueError):
            new_place.update({
                "title": "",
                "description": "A nice place to stay",
                "price": 100.0,
                "latitude": 37.7,
                "longitude": -122.4,
                "owner_id": owner.id})


if __name__ == '__main__':
    unittest.main()
