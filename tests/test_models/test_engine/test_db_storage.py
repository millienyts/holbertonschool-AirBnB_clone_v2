#!/usr/bin/python3
"""
This module contains unit tests for the DBStorage class within the AirBnB clone project.
These tests cover documentation, coding style, and various functional aspects of DBStorage.
"""
from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pycodestyle
import unittest

DBStorage = db_storage.DBStorage
storage_t = os.getenv("HBNB_TYPE_STORAGE")
classes = {"Amenity": Amenity, "City": City, "Place": Place, "Review": Review, "State": State, "User": User}

class TestDBStorageFunctionality(unittest.TestCase):
    """
    Tests the functionality of the DBStorage class to ensure it behaves as expected.
    """
    @unittest.skipIf(storage_t != 'db', "DB storage testing is bypassed unless 'db' storage is used")
    def test_all_returns_dict(self):
        """
        Test that the all method returns a dictionary of objects.
        """
        self.assertIsInstance(models.storage.all(), dict)

    @unittest.skipIf(storage_t != 'db', "DB storage testing is bypassed unless 'db' storage is used")
    def test_all_no_class(self):
        """
        Test that calling all without specifying a class returns all objects in storage.
        """
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(storage_t != 'db', "DB storage testing is bypassed unless 'db' storage is used")
    def test_new(self):
        """
        Test that the new method correctly adds objects to the database.
        """
        # Implementation needed

    @unittest.skipIf(storage_t != 'db', "DB storage testing is bypassed unless 'db' storage is used")
    def test_save(self):
        """
        Test that the save method properly commits objects to the database.
        """
        # Implementation needed

class TestDBStorageDocumentationAndStyle(unittest.TestCase):
    """
    Verifies that the DBStorage class and its tests are properly documented and adhere to PEP8.
    """
    @classmethod
    def setUpClass(cls):
        """
        Prepares for testing documentation and PEP8 compliance.
        """
        cls.dbs_funcs = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """
        Test that db_storage.py conforms to PEP8 standards.
        """
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0, "db_storage.py should follow PEP8.")

    def test_pep8_conformance_test_db_storage(self):
        """
        Test that the DBStorage tests are PEP8 compliant.
        """
        pep8s = pycodestyle.StyleGuide(quiet=True)
        file_path = 'tests/test_models/test_engine/test_db_storage.py'
        result = pep8s.check_files([file_path])
        self.assertEqual(result.total_errors, 0, f"{file_path} should follow PEP8.")

    def test_db_storage_module_docstring(self):
        """
        Test for the presence of a docstring in the db_storage module.
        """
        self.assertTrue(db_storage.__doc__)

    def test_db_storage_class_docstring(self):
        """
        Test for the presence of a docstring in the DBStorage class.
        """
        self.assertTrue(DBStorage.__doc__)

    def test_db_storage_method_docstrings(self):
        """
        Ensure all DBStorage class methods have docstrings.
        """
        for func_name, func in self.dbs_funcs:
            self.assertTrue(func.__doc__, f"{func_name} method needs a docstring")

class TestDBStorageSpecific(unittest.TestCase):
    """
    Focuses on testing specific functionality of the DBStorage class.
    """
    @unittest.skipIf(storage_t != 'db', "These tests only apply when 'db' storage is used.")
    def test_all_returns_dict_for_no_class(self):
        """
        Confirm all() returns a dictionary for all objects when no class is given.
        """
        self.assertIsInstance(models.storage.all(), dict)

    @unittest.skipIf(storage_t != 'db', "These tests only apply when 'db' storage is used.")
    def test_new_adds_object(self):
        """
        Test to ensure new() method adds an object to storage.
        """
        initial_count = len(models.storage.all())
        new_object = list(classes.values())[0]()
        models.storage.new(new_object)
        models.storage.save()
        self.assertTrue(len(models.storage.all()) > initial_count)

    @unittest.skipIf(storage_t != 'db', "These tests only apply when 'db' storage is used.")
    def test_save_updates_storage(self):
        """
        Test to ensure save() properly commits all objects to the database.
        """
        new_object = list(classes.values())[0]()
        models.storage.new(new_object)
        models.storage.save()
        self.assertIn(new_object, models.storage.all(type(new_object)).values())

if __name__ == "__main__":
    unittest.main()
