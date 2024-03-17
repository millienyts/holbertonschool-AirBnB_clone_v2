#!/usr/bin/python3
"""
Module contains tests for verifying the documentation and coding style compliance
of the HBNB console.
"""

import console
import unittest
import pycodestyle
from console import HBNBCommand

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
