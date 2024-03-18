#!/usr/bin/env python3
"""
This module contains tests for the Amenity class from the models module.
"""

# Reordering imports for readability
from datetime import datetime
import unittest
from unittest.mock import patch
from time import sleep
from os import getenv
import pycodestyle
# Importing test modules and classes
from tests.test_models.test_base_model import test_basemodel
from models.base_model import BaseModel
from models.amenity import Amenity

# Environment variable for storage type
storage_t = getenv("HBNB_TYPE_STORAGE")

class TestAmenityModel(test_basemodel):
    """
    Tests the Amenity class for expected behavior and functionality.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initializes the TestAmenityModel class.
        """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name_attribute(self):
        """
        Test the name attribute of the Amenity class.
        """
        new = self.value()
        self.assertEqual(type(new.name), str)

class TestCodeStyle(unittest.TestCase):
    """
    Test for PEP 8 compliance on the Amenity class.
    """
    
    def test_pep8_conformance(self):
        """
        Test that we conform to PEP 8.
        """
        pep8style = pycodestyle.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors (and warnings).")

class TestInheritanceFromBaseModel(unittest.TestCase):
    """
    Test if the Amenity class inherits properly from BaseModel.
    """
    
    def test_is_instance_of_base_model(self):
        """
        Check if an instance of Amenity is also an instance of BaseModel.
        """
        instance = Amenity()
        self.assertIsInstance(instance, BaseModel)
        self.assertTrue(issubclass(type(instance), BaseModel))
        self.assertEqual(str(type(instance)), "<class 'models.amenity.Amenity'>")

class TestAmenityAttributes(unittest.TestCase):
    """
    Test attributes and methods of the Amenity class.
    """
    
    def test_attributes_existence(self):
        """
        Test if the attributes exist and have correct types.
        """
        with patch('models.amenity.Amenity', autospec=True):
            instance = Amenity()
            instance.name = "Pool"
            expected_attrs_types = {
                "id": str,
                "created_at": datetime,
                "updated_at": datetime,
                "name": str,
            }
            instance_dict = instance.to_dict()
            expected_dict_keys = [
                "id",
                "created_at",
                "updated_at",
                "name",
                "__class__"
            ]
            self.assertCountEqual(instance_dict.keys(), expected_dict_keys)
            self.assertEqual(instance_dict['name'], 'Pool')
            self.assertEqual(instance_dict['__class__'], 'Amenity')

            for attr, attr_type in expected_attrs_types.items():
                with self.subTest(attr=attr, attr_type=attr_type):
                    self.assertIn(attr, instance.__dict__)
                    self.assertIs(type(instance.__dict__[attr]), attr_type)
            self.assertEqual(instance.name, "Pool")

    def test_amenity_ids_and_creation_dates(self):
        """
        Test the uniqueness and sequential creation of IDs and creation dates.
        """
        instance1 = Amenity()
        sleep(1)
        instance2 = Amenity()
        sleep(1)
        instance3 = Amenity()
        user_instances = [instance1, instance2, instance3]
        for instance in user_instances:
            with self.subTest(instance_id=instance.id):
                self.assertIs(type(instance.id), str)
        self.assertNotEqual(instance1.id, instance2.id)
        self.assertNotEqual(instance1.id, instance3.id)
        self.assertNotEqual(instance2.id, instance3.id)
        self.assertTrue(instance1.created_at < instance2.created_at < instance3.created_at)

    def test_string_representation(self):
        """
        Test the string representation of Amenity instances.
        """
        instance = Amenity()
        expected_format = "[Amenity] ({}) {}".format(instance.id, instance.__dict__)
        self.assertEqual(expected_format, str(instance))

    @patch('models.storage')
    def test_save_updates_storage(self, mocked_storage):
        """
        Test that the save method updates storage with the correct data.
        """
        instance = Amenity()
        old_created_at = instance.created_at
        sleep(1)
        old_updated_at = instance.updated_at
        instance.save()
        self.assertEqual(old_created_at, instance.created_at)
        self.assertNotEqual(old_updated_at, instance.updated_at)
        self.assertTrue(mocked_storage.save.called)

class TestAmenityAttributes(unittest.TestCase):
    """
    Further tests for the Amenity class's attributes and methods.
    """
    
    def test_is_subclass_of_base_model(self):
        """
        Verify that Amenity is a subclass of BaseModel.
        """
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))

    def test_name_attribute_defaults(self):
        """
        Test the default value of the name attribute based on storage type.
        """
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))
        if storage_t == 'db':
            self.assertIsNone(amenity.name)
        else:
            self.assertEqual(amenity.name, "")

    def test_dictionary_representation(self):
        """
        Test the dictionary representation of an Amenity instance.
        """
        instance = Amenity()
        instance_dict = instance.to_dict()
        self.assertEqual(dict, type(instance_dict))
        self.assertFalse("_sa_instance_state" in instance_dict)
        for attr in instance.__dict__:
            if attr != "_sa_instance_state":
                self.assertIn(attr, instance_dict)
        self.assertIn("__class__", instance_dict)

    def test_dictionary_values(self):
        """
        Ensure the values in the dictionary representation are accurate.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        instance = Amenity()
        instance_dict = instance.to_dict()
        self.assertEqual("Amenity", instance_dict["__class__"])
        self.assertEqual(str, type(instance_dict["created_at"]))
        self.assertEqual(str, type(instance_dict["updated_at"]))
        self.assertEqual(instance.created_at.strftime(time_format), instance_dict["created_at"])
        self.assertEqual(instance.updated_at.strftime(time_format), instance_dict["updated_at"])

    def test_string_output(self):
        """
        Test the string output format of an Amenity instance.
        """
        instance = Amenity()
        expected_output = "[Amenity] ({}) {}".format(instance.id, instance.__dict__)
        self.assertEqual(expected_output, str(instance))

