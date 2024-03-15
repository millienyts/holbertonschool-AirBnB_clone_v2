#!/usr/bin/python3
"""
Module for testing DBStorage
"""
import unittest
import os
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models import storage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

@unittest.skipUnless(os.getenv('HBNB_TYPE_STORAGE') == 'db', "DBStorage tests")
class TestDBStorage(unittest.TestCase):
    """Tests for the DBStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up for the db tests."""
        cls.user = User(email="test@test.com", password="test", first_name="Test", last_name="Test")
        cls.state = State(name="TestState")
        cls.city = City(name="TestCity", state_id=cls.state.id)
        storage.new(cls.user)
        storage.new(cls.state)
        storage.new(cls.city)
        storage.save()

    @classmethod
    def tearDownClass(cls):
        """Tear down for the db tests."""
        storage.delete(cls.user)
        storage.delete(cls.city)
        storage.delete(cls.state)
        storage.save()

    def test_create(self):
        """Test creation of a new instance."""
        initial_count = len(storage.all(User))
        user = User(email="create@test.com", password="password", first_name="First", last_name="Last")
        user.save()
        final_count = len(storage.all(User))
        self.assertNotEqual(initial_count, final_count)

    def test_retrieval(self):
        """Test retrieval of an instance."""
        state = State(name="NewState")
        state.save()
        state_id = state.id
        retrieved_state = storage.all(State)[f'State.{state_id}']
        self.assertEqual(state.name, retrieved_state.name)

    def test_update(self):
        """Test updating of an instance."""
        user = User(email="update@test.com", password="update", first_name="Update", last_name="Test")
        user.save()
        user_id = user.id
        storage.all(User)[f'User.{user_id}'].first_name = "UpdatedName"
        storage.save()
        updated_user = storage.all(User)[f'User.{user_id}']
        self.assertEqual(updated_user.first_name, "UpdatedName")

    def test_deletion(self):
        """Test deletion of an instance."""
        state = State(name="DeleteState")
        state.save()
        initial_count = len(storage.all(State))
        storage.delete(state)
        storage.save()
        final_count = len(storage.all(State))
        self.assertNotEqual(initial_count, final_count)

if __name__ == "__main__":
    unittest.main()
