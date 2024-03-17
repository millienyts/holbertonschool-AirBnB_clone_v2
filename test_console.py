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

            # Additional tests from Code 1
            clear_stream(cout)
            HBNBCommand().onecmd('create User name="James" age=17 height=5.9')
            user_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(user_id), storage.all().keys())
            clear_stream(cout)
            HBNBCommand().onecmd('show User {}'.format(user_id))
            self.assertIn("'name': 'James'", cout.getvalue().strip())
            self.assertIn("'age': 17", cout.getvalue().strip())
            self.assertIn("'height': 5.9", cout.getvalue().strip())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create_show_count(self):
        """Tests the create, show, and count commands with the database storage."""
        with patch('sys.stdout', new_callable=StringIO) as cout:
            HBNBCommand().onecmd('create User email="john25@gmail.com" password="123"')
            user_id = cout.getvalue().strip()
            dbc = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'), port=3306, user=os.getenv('HBNB_MYSQL_USER'), passwd=os.getenv('HBNB_MYSQL_PWD'), db=os.getenv('HBNB_MYSQL_DB'))
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(user_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            cursor.close()
            dbc.close()

            # Testing show command
            user = User(email="ui@example.com", password="pwd")
            user_id = user.id
            user.save()
            clear_stream(cout)
            HBNBCommand().onecmd('show User {}'.format(user_id))
            self.assertIn('ui@example.com', cout.getvalue().strip())
            self.assertIn('pwd', cout.getvalue().strip())

            # Testing count command
            initial_count = storage.count('State')
            HBNBCommand().onecmd('create State name="Lagos"')
            final_count = storage.count('State')
            self.assertEqual(final_count, initial_count + 1)

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

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage tests only')
class TestDBStorageConsole(unittest.TestCase):
    """Tests for DBStorage related console functionality."""

    def setUp(self):
        """Setup test case environment."""
        self.consol = HBNBCommand()

    def tearDown(self):
        """Clean up after each test method."""
        # Delete created objects from database to maintain a clean state
        storage._DBStorage__session.rollback()
        storage._DBStorage__session.close()

    def test_db_create_state(self):
        """Test creating a State via the console with DBStorage."""
        with patch('sys.stdout', new_callable=StringIO) as cout:
            self.consol.onecmd('create State name="California"')
            state_id = cout.getvalue().strip()
            self.assertTrue(state_id)

            # Query the database to ensure the State was created
            state = storage._DBStorage__session.query(State).filter(State.id == state_id).one_or_none()
            self.assertIsNotNone(state)
            self.assertEqual(state.name, "California")

    def test_db_create_user(self):
        """Test creating a User via the console with DBStorage."""
        # Assume User class and email/password fields exist and are valid
        with patch('sys.stdout', new_callable=StringIO) as cout:
            self.consol.onecmd('create User email="test@example.com" password="test"')
            user_id = cout.getvalue().strip()
            self.assertTrue(user_id)
            
if __name__ == "__main__":
    unittest.main()
