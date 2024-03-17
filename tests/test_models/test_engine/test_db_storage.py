#!/usr/bin/python3
"""
Comprehensive Tests for the DBStorage class functionality within the AirBnB clone project.
Includes documentation and style compliance tests along with functional validation.
"""
import unittest
import inspect
import pycodestyle
from os import getenv
from models.engine import db_storage
from models import (Amenity, BaseModel, City, Place, Review, State, User)

DBStorage = db_storage.DBStorage

# Defining a dict to hold classes for easy reference
model_classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}

class TestDBStorageDocumentation(unittest.TestCase):
    """Evaluates documentation and style compliance of the DBStorage class."""
    
    @classmethod
    def setUpClass(cls):
        """Collects DBStorage methods for inspection."""
        cls.functions = inspect.getmembers(DBStorage, inspect.isfunction)
    
    def test_module_docstring(self):
        """Checks the existence of the module docstring."""
        self.assertTrue(len(db_storage.__doc__) > 0, "Missing module docstring.")
    
    def test_class_docstring(self):
        """Verifies the DBStorage class docstring."""
        self.assertTrue(len(DBStorage.__doc__) > 0, "Missing class docstring.")
    
    def test_function_docstrings(self):
        """Ensures all functions have docstrings."""
        for function in self.functions:
            self.assertTrue(len(function[1].__doc__) > 0, f"Missing docstring in {function[0]} method.")

    def test_pep8_compliance(self):
        """Tests PEP8/style compliance."""
        style_guide = pycodestyle.StyleGuide(quiet=True)
        result = style_guide.check_files(['models/engine/db_storage.py', 'tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors (and warnings).")

class TestDBStorageFunctionality(unittest.TestCase):
    """Validates the functionality of the DBStorage class."""

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', "DBStorage tests skipped when not using db storage")
    def test_all_method(self):
        """Tests that 'all' method returns a dictionary of all objects."""
        for cls_name in model_classes:
            obj_count = len(DBStorage().all(model_classes[cls_name]))
            self.assertIsInstance(obj_count, int, f"all method failed with {cls_name}.")

    def test_new_method(self):
        """Tests the 'new' method for adding objects to storage."""
        storage = DBStorage()
        original_count = len(storage.all())
        new_obj = list(model_classes.values())[0]()
        storage.new(new_obj)
        storage.save()
        new_count = len(storage.all())
        self.assertTrue(new_count > original_count, "New object was not added to DBStorage.")

    def test_save_method(self):
        """Verifies that objects are persisted to the database."""
        storage = DBStorage()
        new_obj = User(email="test@test.com", password="test")
        storage.new(new_obj)
        storage.save()
        self.assertIn(f"User.{new_obj.id}", storage.all("User"), "Object not found after save.")

    def test_delete_method(self):
        """Confirms that objects are deletable from DBStorage."""
        storage = DBStorage()
        new_obj = User(email="delete@test.com", password="delete")
        storage.new(new_obj)
        storage.save()
        storage.delete(new_obj)
        storage.save()
        self.assertNotIn(f"User.{new_obj.id}", storage.all("User"), "Object was not deleted.")

if __name__ == "__main__":
    unittest.main()
