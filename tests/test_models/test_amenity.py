#!/usr/bin/python3
"""
Test suite for the Amenity class in the AirBnB clone project.
This suite tests everything from initialization and attribute assignment to serialization and PEP8 compliance.
"""

from models.base_model import BaseModel
from models.amenity import Amenity
import unittest
from unittest.mock import patch
from time import sleep
import pycodestyle
from datetime import datetime
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")


class TestAmenityAttributes(unittest.TestCase):
    """
    Test cases for the Amenity model attributes and their types.
    """

    def setUp(self):
        """
        Initialize a new Amenity instance before each test.
        """
        self.amenity = Amenity()
        self.amenity.name = "Pool"

    def tearDown(self):
        """
        Delete the Amenity instance after each test.
        """
        del self.amenity

    def test_amenity_inherits_base_model(self):
        """
        Test if Amenity is a subclass of BaseModel.
        """
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_amenity_attributes(self):
        """
        Test the Amenity attributes and their types.
        """
        self.assertTrue(hasattr(Amenity, "name"))
        self.assertIsInstance(self.amenity.name, str)


class TestAmenityMethods(unittest.TestCase):
    """
    Test cases for Amenity model methods.
    """

    def test_amenity_to_dict(self):
        """
        Test conversion of Amenity instance to dictionary format.
        """
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(amenity_dict['__class__'], 'Amenity')
        self.assertIsInstance(amenity_dict['created_at'], str)
        self.assertIsInstance(amenity_dict['updated_at'], str)

    def test_amenity_str_representation(self):
        """
        Test the string representation of the Amenity instance.
        """
        amenity = Amenity(name="WiFi")
        str_format = f"[Amenity] ({amenity.id}) {amenity.__dict__}"
        self.assertEqual(str(amenity), str_format)


class TestAmenityPEP8(unittest.TestCase):
    """
    Test cases to check PEP8 compliance of the amenity model.
    """

    def test_pep8_compliance(self):
        """
        Test that amenity.py is in compliance with PEP8 guidelines.
        """
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors or warnings.")


class TestAmenityStorage(unittest.TestCase):
    """
    Test cases for storage related operations of the Amenity model.
    """

    @patch('models.storage')
    def test_save_method_calls_storage_save(self, mock_storage):
        """
        Test if saving an Amenity instance calls the storage save method.
        """
        amenity = Amenity()
        amenity.save()
        self.assertTrue(mock_storage.save.called)
