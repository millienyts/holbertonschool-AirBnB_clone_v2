#!/usr/bin/python3
"""A unit test module for the console (command interpreter).
"""
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
    """
    Tests to assess the documentation and coding style of the console application.
    """
    
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

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests the create command with the database storage."""
        with patch('sys.stdout', new_callable=StringIO) as cout:
            HBNBCommand().onecmd('create User email="john25@gmail.com" password="123"')
            mdl_id = cout.getvalue().strip()
            dbc = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'), port=3306, user=os.getenv('HBNB_MYSQL_USER'), passwd=os.getenv('HBNB_MYSQL_PWD'), db=os.getenv('HBNB_MYSQL_DB'))
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(mdl_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            cursor.close()
            dbc.close()

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show command with the database storage."""
        user = User(email="ui@example.com", password="pwd")
        user_id = user.id
        user.save()
        with patch('sys.stdout', new_callable=StringIO) as cout:
            HBNBCommand().onecmd('show User {}'.format(user_id))
            self.assertIn('ui@example.com', cout.getvalue().strip())
            self.assertIn('pwd', cout.getvalue().strip())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command with the database storage."""
        initial_count = storage.count('State')
        HBNBCommand().onecmd('create State name="Lagos"')
        final_count = storage.count('State')
        self.assertEqual(final_count, initial_count + 1)
class TestDBStorageConsole(unittest.TestCase):
    """Tests for DBStorage related console functionality."""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create_user(self):
        """Test creating a User object with DBStorage through the console."""
        with patch('sys.stdout', new_callable=StringIO) as cout:
            # Create a new User via the console with specific attributes
            HBNBCommand().onecmd('create User email="test@example.com" password="pwd" first_name="Test" last_name="User"')
            user_id = cout.getvalue().strip()
            self.assertTrue(user_id)

            # Connect to the database to verify the User has been created
            conn = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                                   user=os.getenv('HBNB_MYSQL_USER'),
                                   passwd=os.getenv('HBNB_MYSQL_PWD'),
                                   db=os.getenv('HBNB_MYSQL_DB'))
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            result = cur.fetchone()
            self.assertIsNotNone(result)
            # Ensure the attributes match
            self.assertEqual(result[1], "test@example.com")  # Assuming email is the second column
            self.assertEqual(result[2], "pwd")  # Assuming password is the third column
            self.assertEqual(result[3], "Test")  # Assuming first_name is the fourth column
            self.assertEqual(result[4], "User")  # Assuming last_name is the fifth column

            cur.close()
            conn.close()

    # Additional DBStorage tests can follow the same pattern, focusing on other operations (update, delete, etc.)

if __name__ == "__main__":
    unittest.main()
