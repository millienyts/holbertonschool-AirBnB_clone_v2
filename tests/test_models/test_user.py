#!/usr/bin/python3
"""Unit tests for the User class."""
import unittest
import os
from models import storage
from models.user import User

class TestUser(unittest.TestCase):
    """Test cases for the User model."""
    
    @classmethod
    def setUpClass(cls):
        """Set up resources before any test cases are run."""
        storage.delete_all()  # Ensures a clean slate for tests that follow.
    
    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all test cases have run."""
        storage.save()

    def setUp(self):
        """Set up resources before each test case."""
        self.user = User()
        self.user.first_name = "Test"
        self.user.last_name = "User"
        self.user.email = "test@example.com"
        self.user.password = "password"

    def tearDown(self):
        """Clean up resources after each test case."""
        del self.user
        storage.save()

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "skip if database storage")
    def test_attributes_file_storage(self):
        """Test model attributes with FileStorage."""
        self.assertEqual(type(self.user.first_name), str)
        self.assertEqual(type(self.user.last_name), str)
        self.assertEqual(type(self.user.email), str)
        self.assertEqual(type(self.user.password), str)

    @unittest.skipUnless(os.getenv('HBNB_TYPE_STORAGE') == 'db', "run only if database storage")
    def test_attributes_db_storage(self):
        """Test model attributes with DBStorage."""
        # Similar tests can go here, but might include database-specific tests
        # such as checking for existence of the user in the database.
        self.assertEqual(type(self.user.first_name), str)
        self.assertEqual(type(self.user.last_name), str)
        self.assertEqual(type(self.user.email), str)
        self.assertEqual(type(self.user.password), str)

        # Example of a DB-specific test (You'd need to adapt it to your setup)
        # Make sure to import necessary modules if you use an ORM like SQLAlchemy
        # self.assertTrue(self.user in storage.session)

if __name__ == "__main__":
    unittest.main()

