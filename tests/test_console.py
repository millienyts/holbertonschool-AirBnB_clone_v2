#!/usr/bin/python3
"""A unit test module for the console (command interpreter)."""
import json
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch
import pycodestyle

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream
import sys

class TestFileStorageConsole(unittest.TestCase):
    """Tests for FileStorage related console functionality."""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create_persistence(self):
        """Test object creation and persistence with FileStorage."""
        with patch('sys.stdout', new_callable=StringIO) as cout:
            # Create a new City via the console
            HBNBCommand().onecmd('create City name="San Francisco"')
            city_id = cout.getvalue().strip()
            self.assertTrue(city_id)

            # Save to ensure the object is written to file
            HBNBCommand().onecmd('save')

            # Clear FileStorage's memory to simulate a new session
            storage.reload()

            # Verify the object persists after reloading
            self.assertIn(f'City.{city_id}', storage.all().keys())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_save_reload_object(self):
        """Test saving and reloading an object with FileStorage."""
        obj_id = ''
        with patch('sys.stdout', new_callable=StringIO) as cout:
            # Create a new object via the console
            HBNBCommand().onecmd('create BaseModel name="Test Reload"')
            obj_id = cout.getvalue().strip()
        
        # Ensure the object ID was captured
        self.assertTrue(obj_id)

        # Invoke save and then reload
        HBNBCommand().onecmd('save')
        storage.reload()

        # Confirm the object is still present after reload
        key = f'BaseModel.{obj_id}'
        all_objs = storage.all()
        self.assertIn(key, all_objs)
        self.assertEqual(all_objs[key].name, "Test Reload")


class TestConsoleDocs(unittest.TestCase):
    """Tests to assess the documentation and coding style of the console application."""
    
    def test_pycodestyle_conformance_console(self):
        """Test that console.py conforms to PEP8/pycodestyle."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0, "console.py does not follow PEP8 guidelines.")

    def test_pycodestyle_conformance_test_console(self):
        """Test that the console tests conform to PEP8/pycodestyle."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0, "tests/test_console.py does not follow PEP8 guidelines.")

    def test_console_module_docstring_exists(self):
        """Check for existence of console.py module docstring."""
        self.assertIsNotNone(console.__doc__, "console.py module lacks a docstring.")

    def test_HBNBCommand_class_docstring_exists(self):
        """Check for existence of the HBNBCommand class docstring."""
        self.assertIsNotNone(HBNBCommand.__doc__, "HBNBCommand class lacks a docstring.")

class TestHBNBCommand(unittest.TestCase):

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test only')
    def test_fs_create_user(self):
        """Test creating a User via the console with FileStorage."""
        with patch('sys.stdout', new_callable=StringIO) as cout:
            HBNBCommand().onecmd("create User email='fs_test@example.com' password='fs_test'")
            user_id = cout.getvalue().strip()
            self.assertTrue(user_id)

            # Verify the new User exists in FileStorage
            user_key = f"User.{user_id}"
            self.assertIn(user_key, storage.all().keys())

            # Fetch the object and verify its attributes
            user_obj = storage.all()[user_key]
            self.assertEqual(user_obj.email, 'fs_test@example.com')

            # Cleanup: remove the created object to avoid test side-effects
            del storage.all()[user_key]
            storage.save()
    """Represents the test class for the HBNBCommand class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up resources before any tests are run."""
        cls.consol = HBNBCommand()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests have run."""
        del cls.consol
    
    def setUp(self):
        """Set up the test environment before each test."""
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        """Clean up after each test."""
        sys.stdout = self.held

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """Tests the create command with the file storage."""
        with patch('sys.stdout', new_callable=StringIO) as cout:
            HBNBCommand().onecmd('create City name="Texas"')
            mdl_id = cout.getvalue().strip()
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            HBNBCommand().onecmd('show City {}'.format(mdl_id))
            self.assertIn('name="Texas"', cout.getvalue().strip())

 # Below are the added DBStorage tests

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests the create command with the database storage."""
        # The setup assumes that environment variables are correctly set for DBStorage
        with patch('sys.stdout', new_callable=StringIO) as cout:
            HBNBCommand().onecmd('create User email="john25@gmail.com" password="123"')
            user_id = cout.getvalue().strip()
            # Verify that the new user exists in the database
            # Note: Adjust the database connection parameters as necessary
            db_conn = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'), 
                                      user=os.getenv('HBNB_MYSQL_USER'), 
                                      passwd=os.getenv('HBNB_MYSQL_PWD'), 
                                      db=os.getenv('HBNB_MYSQL_DB'))
            cursor = db_conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM users WHERE id = '{user_id}'")
            result = cursor.fetchone()
            self.assertTrue(result[0] > 0, "User was not created in the database")
            cursor.close()
            db_conn.close()

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show command for an object in database storage."""
        # Implement similarly to test_db_create, verifying object retrieval

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_destroy(self):
        """Tests the destroy command for an object in database storage."""
        # Implement test logic here, ensuring object deletion is reflected in the database

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_all(self):
        """Tests the all command with DBStorage."""
        # Implement test to verify 'all' command functionality with DBStorage

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_update(self):
        """Tests the update command with DBStorage."""
        # Implement test to verify 'update' command functionality with DBStorage

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command with the database storage."""
        initial_count = storage.count('State')
        HBNBCommand().onecmd('create State name="Lagos"')
        final_count = storage.count('State')
        self.assertEqual(final_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_destroy(self):
        """Test object destruction with FileStorage."""
        with patch('sys.stdout', new_callable=StringIO) as cout:
            # Create a new User via the console to ensure we have an object to delete
            HBNBCommand().onecmd('create User name="Test User"')
            user_id = cout.getvalue().strip()

            # Ensure the User object was created
            self.assertTrue(user_id)
            self.assertIn(f'User.{user_id}', storage.all().keys())

            # Destroy the created User object
            HBNBCommand().onecmd(f'destroy User {user_id}')

            # Ensure the User object is no longer present
            self.assertNotIn(f'User.{user_id}', storage.all().keys())

if __name__ == "__main__":
    unittest.main()
