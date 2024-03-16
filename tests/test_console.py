#!/usr/bin/python3
"""Test suite for the console."""

import sys
import os
from io import StringIO
import unittest
from unittest.mock import patch
from console import HBNBCommand

class TestConsole(unittest.TestCase):
    """Tests the console module."""

    def setUp(self):
        """Set up redirecting stdout to capture print outputs."""
        self.capturedOutput = StringIO()
        sys.stdout = self.capturedOutput

    def tearDown(self):
        """Clean up by resetting stdout."""
        sys.stdout = sys.__stdout__

    def create_console(self):
        """Helper method to create a console instance."""
        return HBNBCommand()

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'file', "skip if not FileStorage")
    @patch('models.storage')
    def test_quit(self, mock_storage):
        """Test if 'quit' command exists."""
        console = self.create_console()
        self.assertTrue(console.onecmd("quit"))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'file', "skip if not FileStorage")
    @patch('models.storage')
    def test_EOF(self, mock_storage):
        """Test if 'EOF' command exists."""
        console = self.create_console()
        self.assertTrue(console.onecmd("EOF"))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'file', "skip if not FileStorage")
    @patch('models.storage')
    def test_all(self, mock_storage):
        """Test 'all' command output type."""
        console = self.create_console()
        console.onecmd("all")
        self.assertIsInstance(self.capturedOutput.getvalue(), str)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'file', "skip if not FileStorage")
    @patch('models.storage')
    def test_create_show_flow(self, mock_storage):
        """Test 'create' and 'show' command flow."""
        console = self.create_console()
        mock_storage.new.return_value.id = "12345"
        console.onecmd("create User")
        user_id = self.capturedOutput.getvalue().strip()

        self.capturedOutput.truncate(0)
        self.capturedOutput.seek(0)

        console.onecmd(f"show User {user_id}")
        self.assertTrue(isinstance(self.capturedOutput.getvalue(), str))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'file', "skip if not FileStorage")
    @patch('models.storage')
    def test_error_messages(self, mock_storage):
        """Test various error messages for 'show' and 'create'."""
        console = self.create_console()

        console.onecmd("create")
        self.assertEqual("** class name missing **\n", self.capturedOutput.getvalue().strip())

        self.capturedOutput.truncate(0)
        self.capturedOutput.seek(0)

        console.onecmd("create Binita")
        self.assertEqual("** class doesn't exist **\n", self.capturedOutput.getvalue().strip())

        self.capturedOutput.truncate(0)
        self.capturedOutput.seek(0)

        console.onecmd("show")
        self.assertEqual("** class name missing **\n", self.capturedOutput.getvalue().strip())

        self.capturedOutput.truncate(0)
        self.capturedOutput.seek(0)

        console.onecmd("show User")
        self.assertEqual("** instance id missing **\n", self.capturedOutput.getvalue().strip())

        self.capturedOutput.truncate(0)
        self.capturedOutput.seek(0)

        console.onecmd("show User 123456")
        self.assertEqual("** no instance found **\n", self.capturedOutput.getvalue().strip())

if __name__ == "__main__":
    unittest.main()
