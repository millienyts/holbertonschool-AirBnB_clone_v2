#!/usr/bin/python3
"""
Module contains tests for verifying the documentation and coding style compliance
of the HBNB console.
"""

import console
import unittest
import pycodestyle
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
from models import storage
from models.base_model import BaseModel

class TestConsoleDocs(unittest.TestCase):
    """
    Tests to assess the documentation and coding style of the console application.
    """

    def test_pycodestyle_conformance_console(self):
        """Test that console.py conforms to PEP8/pycodestyle."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "console.py does not follow PEP8 guidelines.")

    def test_pycodestyle_conformance_test_console(self):
        """Test that the console tests conform to PEP8/pycodestyle."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "tests/test_console.py does not follow PEP8 guidelines.")

    def test_console_module_docstring_exists(self):
        """Check for existence of console.py module docstring."""
        self.assertIsNotNone(console.__doc__,
                             "console.py module lacks a docstring.")

    def test_HBNBCommand_class_docstring_exists(self):
        """Check for existence of the HBNBCommand class docstring."""
        self.assertIsNotNone(HBNBCommand.__doc__,
                             "HBNBCommand class lacks a docstring.")

class TestConsoleFunctionality(unittest.TestCase):
    """Tests for the functionality of the HBNB console."""

    def setUp(self):
        """Set up the test environment before each test."""
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        """Clean up after each test."""
        sys.stdout = self.held
        storage.delete_all()

def test_do_create_with_parameters(self):
    """Test creating an object via the console with initial parameters."""
    with patch('sys.stdout', new_callable=StringIO) as mocked_stdout:
        # Simulate 'create' command with initial parameters
        command = 'create BaseModel name="Test" number=100'
        HBNBCommand().onecmd(command)
        output = mocked_stdout.getvalue().strip()
        # Extracting object ID from the command output
        obj_id = output.split('\n')[-1]
        self.assertIsNotNone(obj_id)

        # Constructing the key for storage validation
        obj_key = f"BaseModel.{obj_id}"
        self.assertIn(obj_key, storage.all())

        # Fetching the object from FileStorage and validating attributes
        obj = storage.all()[obj_key]
        self.assertEqual(getattr(obj, "name", None), "Test")
        self.assertEqual(getattr(obj, "number", None), 100)


if __name__ == "__main__":
    unittest.main()
