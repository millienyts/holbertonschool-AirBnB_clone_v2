#!/usr/bin/python3
"""Unit tests for DBStorage."""
import unittest
import pep8
from models import (BaseModel, User, State, City, Amenity, Place, Review, 
                    engine, storage)
from models.engine.db_storage import DBStorage
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

class DBStorageTestCase(unittest.TestCase):
    """Tests for DBStorage functionality."""

    @classmethod
    def setUpClass(cls):
        """Setting up resources before any DBStorage tests."""
        if isinstance(storage, DBStorage):
            cls.engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'.
                                       format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_DB')),
                                       pool_pre_ping=True)
            Base.metadata.create_all(cls.engine)
            Session = sessionmaker(bind=cls.engine)
            cls.session = Session()
            cls.setupTestData()

    @classmethod
    def tearDownClass(cls):
        """Cleanup resources after all DBStorage tests."""
        if isinstance(storage, DBStorage):
            cls.session.close()
            Base.metadata.drop_all(cls.engine)

    @classmethod
    def setupTestData(cls):
        """Create test data."""
        cls.test_user = User(email='test@test.com', password='testPwd')
        cls.session.add(cls.test_user)
        cls.test_state = State(name='TestState')
        cls.session.add(cls.test_state)
        cls.session.commit()

    def test_pep8_conformance(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8_style = pep8.StyleGuide(quiet=True)
        result = pep8_style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0, "Code should be PEP8 compliant.")

    def test_documentation(self):
        """Test for existence of module and method documentation."""
        self.assertIsNotNone(DBStorage.__doc__, "Module docstring required.")
        self.assertIsNotNone(DBStorage.all.__doc__, "Method docstring required.")

    def test_db_storage_all_method(self):
        """Test retrieval of all objects of a certain class from DB."""
        all_states = storage.all(State)
        self.assertIsInstance(all_states, dict, "Should return a dictionary.")

    def test_db_storage_new_method(self):
        """Test addition of an object to the database."""
        new_state = State(name='NewState')
        self.session.add(new_state)
        self.session.commit()
        self.assertIn('State.{}'.format(new_state.id), storage.all(State))

    def test_db_storage_save_method(self):
        """Test commit of all changes to the database."""
        new_user = User(email='save@test.com', password='savePwd')
        self.session.add(new_user)
        self.session.commit()
        self.assertIn('User.{}'.format(new_user.id), storage.all(User))

    def test_db_storage_delete_method(self):
        """Test deletion of an object from the database."""
        deletable = User(email='delete@test.com', password='deletePwd')
        self.session.add(deletable)
        self.session.commit()
        self.session.delete(deletable)
        self.session.commit()
        self.assertNotIn('User.{}'.format(deletable.id), storage.all(User))

if __name__ == '__main__':
    unittest.main()
