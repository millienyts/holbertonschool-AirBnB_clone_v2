#!/usr/bin/python3
"""
Unit tests for the DBStorage class in the AirBnB clone project.
Combines documentation, style, and functional tests.
"""
from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.base_model import BaseModel
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

DBStorage = db_storage.DBStorage
storage_t = os.getenv("HBNB_TYPE_STORAGE")
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}

class TestDBStorageDocs(unittest.TestCase):
    """Tests to ensure documentation and style compliance for the DBStorage class."""
    # Your existing doc and style tests here...

class TestDBStorage(unittest.TestCase):
    """Tests for specific DBStorage functionality."""
    # Your existing DBStorage functionality tests here...

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_delete(self):
        """Test the delete method removes an object from the database."""
        state = State(name="California")
        models.storage.new(state)
        models.storage.save()
        models.storage.delete(state)
        models.storage.save()
        self.assertNotIn(state, models.storage.all(State))

    @unittest.skipIf(storage_t != 'db', "DB storage tests only applicable if storage type is 'db'")
    def test_reload(self):
        """Test the reload method properly loads objects from the database."""
        initial_count = len(models.storage.all(State))
        # Assuming a State object has been added directly to DB in setUpClass or a previous test
        models.storage.reload()
        self.assertTrue(len(models.storage.all(State)) >= initial_count)

# Consider adding more tests here for coverage...

if __name__ == "__main__":
    unittest.main()
