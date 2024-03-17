#!/usr/bin/python3
"""
Module for testing the Place class.
"""
from tests.test_models.test_base_model import TestBaseModel
from models.place import Place
from models import storage

import os

class TestPlace(TestBaseModel):
    """Tests for the Place class."""

    def __init__(self, *args, **kwargs):
        """Initializes the TestPlace class."""
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """Test the type of Place city_id attribute."""
        new = self.value()
        expected_type = str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.city_id), expected_type)

    def test_user_id(self):
        """Test the type of Place user_id attribute."""
        new = self.value()
        self.assertEqual(type(new.user_id), expected_type)

    def test_name(self):
        """Test the type of Place name attribute."""
        new = self.value()
        self.assertEqual(type(new.name), expected_type)

    def test_description(self):
        """Test the type of Place description attribute."""
        new = self.value()
        self.assertEqual(type(new.description), expected_type)

    def test_number_rooms(self):
        """Test the type of Place number_rooms attribute."""
        new = self.value()
        self.assertEqual(type(new.number_rooms), int if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_number_bathrooms(self):
        """Test the type of Place number_bathrooms attribute."""
        new = self.value()
        self.assertEqual(type(new.number_bathrooms), expected_type)

    def test_max_guest(self):
        """Test the type of Place max_guest attribute."""
        new = self.value()
        self.assertEqual(type(new.max_guest), expected_type)

    def test_price_by_night(self):
        """Test the type of Place price_by_night attribute."""
        new = self.value()
        self.assertEqual(type(new.price_by_night), expected_type)

    def test_latitude(self):
        """Test the type of Place latitude attribute."""
        new = self.value()
        self.assertEqual(type(new.latitude), float if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))

    def test_longitude(self):
        """Test the type of Place longitude attribute."""
        new = self.value()
        self.assertEqual(type(new.longitude), expected_type)

    def test_amenity_ids(self):
        """Test the type of Place amenity_ids attribute."""
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None))
