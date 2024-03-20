#!/usr/bin/python3
"""
Unit tests for the DBStorage class in the AirBnB clone project.
Combines documentation, style, and functional tests.
"""
from datetime import datetime
import inspect
import models
from models.engine.db_storage import DBStorage
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pycodestyle
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

storage_t = os.getenv("HBNB_TYPE_STORAGE")
if storage_t == 'db':
    models.storage.reload()

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
        self.assertEqual(result.total_errors, 0,
                         "Found style errors or warnings.")

    def test_pycodestyle_conformance_test_db_storage(self):
        """Check tests for db_storage for PEP8/pycodestyle compliance."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found style errors or warnings in tests.")

    def test_db_storage_module_docstring(self):
        """Validate the db_storage.py module's docstring."""
        self.assertIsNotNone(models.engine.db_storage.__doc__,
                             "db_storage.py module lacks a docstring.")

    def test_db_storage_class_docstring(self):
        """Validate the DBStorage class's docstring."""
        self.assertIsNotNone(
            DBStorage.__doc__, "DBStorage class lacks a docstring.")

    def test_dbs_func_docstrings(self):
        """Ensure all DBStorage methods have docstrings."""
        for func in self.dbs_funcs:
            self.assertIsNotNone(func[1].__doc__, f"The {
                                 func[0]} method lacks a docstring.")


class TestDBStorage(unittest.TestCase):
    """Tests for specific DBStorage functionality."""

    @classmethod
    def setUpClass(cls):
        """Prepare for tests. Only runs when DB storage is used."""
        if storage_t == 'db':
            cls.storage = DBStorage()
            cls.engine = cls.storage._DBStorage__engine
            Base.metadata.create_all(cls.engine)
            cls.session = scoped_session(sessionmaker(bind=cls.engine))()

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests have run. Only runs when DB storage is used."""
        if storage_t == 'db':
            Base.metadata.drop_all(cls.engine)
            cls.session.remove()

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_all_returns_dict(self):
        """Verify that calling all without arguments returns a dictionary."""
        self.assertIsInstance(models.storage.all(), dict,
                              "all() should return a dictionary.")

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_delete(self):
        """Test that delete properly removes an object from the database."""
        new_state = State(name="DeleteTest")
        models.storage.new(new_state)
        models.storage.save()
        self.assertIn(new_state, models.storage.all(State).values())
        models.storage.delete(new_state)
        models.storage.save()
        self.assertNotIn(new_state, models.storage.all(State).values())

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_create_new_object(self):
        """Test creating a new object and saving it to the database."""
        initial_count = len(models.storage.all(User))
        new_user = User(email="test@example.com", password="test")
        models.storage.new(new_user)
        models.storage.save()
        final_count = len(models.storage.all(User))
        self.assertEqual(final_count, initial_count + 1,
                         "Failed to create a new User object in the database")

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_reload(self):
        """Test reloading objects from the database."""
        models.storage.reload()
        self.assertIsNotNone(models.storage._DBStorage__session,
                             "Session should be initialized on reload")

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_delete(self):
        """Test that delete properly removes an object from the database."""
        new_state = State(name="DeleteTest")
        models.storage.new(new_state)
        models.storage.save()
        self.assertIn(new_state, models.storage.all(State).values())
        models.storage.delete(new_state)
        models.storage.save()
        self.assertNotIn(new_state, models.storage.all(State).values())

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_create_new_object(self):
        """Test creating a new object and saving it to the database."""
        initial_count = len(models.storage.all(User))
        new_user = User(email="test@example.com", password="test")
        models.storage.new(new_user)
        models.storage.save()
        final_count = len(models.storage.all(User))
        self.assertEqual(final_count, initial_count + 1,
                         "Failed to create a new User object in the database")

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_reload(self):
        """Test reloading objects from the database."""
        # Note: Implementation may vary based on how you handle session management
        models.storage.reload()
        self.assertIsNotNone(models.storage._DBStorage__session,
                             "Session should be initialized on reload")


if __name__ == "__main__":
    unittest.main()
