import unittest
from app import create_app
from app.models.amenity import Amenity


class TestUserEndpoints(unittest.TestCase):
    """Unit tests for Amenity API endpoints."""

    def setUp(self):
        """Set up the test client before each test."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        """Test creating a new amenity with valid data succeeds (201)."""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_empty_amenity(self):
        """Test creating an amenity with empty name raises ValueError."""
        self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertRaises(ValueError)

    def test_create_same_amenity(self):
        """Test creating an amenity with a duplicate name returns 400."""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        """Test retrieving all amenities returns status 200."""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test_valid_update_amenity(self):
        """Test updating an amenity with valid data succeeds."""
        new_amenity = Amenity("Wi-Fi")
        new_amenity.update({"name": "Jacuzzi"})
        self.assertEqual(new_amenity.name, "Jacuzzi")

    def test_invalid_update_amenity(self):
        """Test updating an amenity with an empty name raises ValueError."""
        new_amenity = Amenity("Wi-Fi")
        with self.assertRaises(ValueError):
            new_amenity.update({"name": ""})


if __name__ == '__main__':
    unittest.main()
