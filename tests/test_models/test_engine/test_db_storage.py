"""
Unit tests for the DBStorage class in the AirBnB clone project.
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

classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}

class TestDBStorageDocs(unittest.TestCase):
    """Tests to ensure documentation and style compliance for the DBStorage class."""

    @classmethod
    def setUpClass(cls):
        """Prepare for docstring tests."""
        cls.dbs_funcs = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pycodestyle_conformance_db_storage(self):
        """Check models/engine/db_storage.py for PEP8/pycodestyle compliance."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0, "Found style errors or warnings.")

    def test_pycodestyle_conformance_test_db_storage(self):
        """Check tests for db_storage for PEP8/pycodestyle compliance."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0, "Found style errors or warnings in tests.")

    def test_db_storage_module_docstring(self):
        """Validate the db_storage.py module's docstring."""
        self.assertIsNotNone(db_storage.__doc__, "db_storage.py module lacks a docstring.")

    def test_db_storage_class_docstring(self):
        """Validate the DBStorage class's docstring."""
        self.assertIsNotNone(DBStorage.__doc__, "DBStorage class lacks a docstring.")

    def test_dbs_func_docstrings(self):
        """Ensure all DBStorage methods have docstrings."""
        for func in self.dbs_funcs:
            self.assertIsNotNone(func[1].__doc__, f"The {func[0]} method lacks a docstring.")

class TestDBStorage(unittest.TestCase):
    """Tests for specific DBStorage functionality."""

    @unittest.skipIf(models.storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_all_returns_dict(self):
        """Verify that calling all without arguments returns a dictionary."""
        self.assertIsInstance(models.storage.all(), dict, "all() should return a dictionary.")

    @unittest.skipIf(models.storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_all_no_class(self):
        """Test all method returns all rows when no class is provided."""
        for class_name in classes:
            self.assertIn(class_name, [obj.__class__.__name__ for obj in models.storage.all().values()], 
                          f"Instances of {class_name} are expected in the dictionary returned by all() without arguments.")

    @unittest.skipIf(models.storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_new(self):
        """Test that new adds an object to the database."""
        for class_name in classes:
            instance = classes[class_name]()
            models.storage.new(instance)
            models.storage.save()
            self.assertIn(instance, models.storage.all(classes[class_name]).values(), 
                          f"Instance of {class_name} should be in DB after new() and save().")

    @unittest.skipIf(models.storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_save(self):
        """Ensure save method properly saves objects to the database."""
        initial_count = len(models.storage.all())
        instance = list(classes.values())[0]()
        models.storage.new(instance)
        models.storage.save()
        self.assertGreater(len(models.storage.all()), initial_count, 
                           "Number of objects in storage should increase after save().")
