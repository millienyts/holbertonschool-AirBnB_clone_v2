#!/usr/bin/python3
"""
Unit tests for the DBStorage class in the AirBnB clone project.
Combines documentation, style, and functional tests.
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
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}

class TestFileStorage(unittest.TestCase):
"""Test the FileStorage class"""
     @unittest.skipIf(storage_t != 'db', "not testing db storage")
     def test_all_returns_dict(self):
         """Test that all returns a dictionaty"""
         self.assertIs(type(models.storage.all()), dict)

     @unittest.skipIf(storage_t != 'db', "not testing db storage")
     def test_all_no_class(self):
         """Test that all returns all rows when no class is passed"""

     @unittest.skipIf(storage_t != 'db', "not testing db storage")
     def test_new(self):
         """test that new adds an object to the database"""

     @unittest.skipIf(storage_t != 'db', "not testing db storage")
     def test_save(self):
         """Test that save properly saves objects to file.json"""

class TestDBStorageDocs(unittest.TestCase):
    """Tests to ensure documentation and style compliance for the DBStorage class."""
    
    @classmethod
    def setUpClass(cls):
        """Prepare for docstring tests."""
        cls.dbs_funcs = inspect.getmembers(DBStorage, inspect.isfunction)
        
   def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")
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
    
    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_all_returns_dict(self):
        """Verify that calling all without arguments returns a dictionary."""
        self.assertIsInstance(models.storage.all(), dict, "all() should return a dictionary.")

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_all_no_class(self):
        """Test all method returns all rows when no class is provided."""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_new(self):
        """Test that new adds an object to the database."""
        instance = list(classes.values())[0]()
        models.storage.new(instance)
        models.storage.save()
        self.assertIn(instance, models.storage.all(type(instance)).values())

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_save(self):
        """Ensure save method properly saves objects to file.json."""
        initial_count = len(models.storage.all())
        instance = list(classes.values())[0]()
        models.storage.new(instance)
        models.storage.save()
        self.assertGreater(len(models.storage.all()), initial_count)

if __name__ == "__main__":
    unittest.main()ls
