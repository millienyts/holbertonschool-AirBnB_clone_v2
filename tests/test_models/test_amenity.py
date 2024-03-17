#!/usr/bin/python3
"""
Module for testing the Amenity class
"""
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
import os

class TestAmenity(test_basemodel):
    """Defines tests for the Amenity class."""

    def __init__(self, *args, **kwargs):
        """Initializes the TestAmenity class."""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """Test the type of name."""
        new = self.value()
        expected_type = str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.name), expected_type, "Incorrect type for 'name' attribute.")
