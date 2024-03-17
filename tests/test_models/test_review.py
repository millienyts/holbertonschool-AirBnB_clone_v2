"""Unit tests for the Review class in the AirBnB clone project."""

from tests.test_models.test_base_model import test_basemodel
from models.review import Review
import unittest

class TestReview(test_basemodel):
    """Test suite for validating the Review model's functionality."""

    def __init__(self, *args, **kwargs):
        """Initialize with Review model test setup."""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_attribute_types(self):
        """Test if instances have expected attributes and their types are correct."""
        new_instance = self.value()
        expected_attributes = {
            "place_id": str,
            "user_id": str,
            "text": str,
        }

        for attribute, expected_type in expected_attributes.items():
            with self.subTest(attribute=attribute):
                self.assertTrue(hasattr(new_instance, attribute), f"{attribute} is missing.")
                self.assertIsInstance(getattr(new_instance, attribute), expected_type, 
                                      f"{attribute} does not match the expected type {expected_type}.")

if __name__ == "__main__":
    unittest.main()
