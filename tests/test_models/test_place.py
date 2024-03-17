"""Unit tests for the Place class in the AirBnB clone project."""

from tests.test_models.test_base_model import test_basemodel
from models.place import Place
import unittest

class TestPlace(test_basemodel):
    """Test suite for the Place model functionality."""

    def __init__(self, *args, **kwargs):
        """Initialize with Place model test setup."""
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_attributes_existence(self):
        """Test if instances have expected attributes and their types."""
        new_instance = self.value()
        attributes_and_types = {
            "city_id": str,
            "user_id": str,
            "name": str,
            "description": str,
            "number_rooms": int,
            "number_bathrooms": int,
            "max_guest": int,
            "price_by_night": int,
            "latitude": float,
            "longitude": float,
            "amenity_ids": list
        }

        for attribute, attr_type in attributes_and_types.items():
            with self.subTest(attribute=attribute):
                self.assertTrue(hasattr(new_instance, attribute))
                self.assertIsInstance(getattr(new_instance, attribute, None), attr_type)

    def test_latitude_longitude_types(self):
        """Test latitude and longitude attributes separately for better clarity."""
        new_instance = self.value()
        self.assertIsInstance(new_instance.latitude, float)
        self.assertIsInstance(new_instance.longitude, float)

if __name__ == "__main__":
    unittest.main()
