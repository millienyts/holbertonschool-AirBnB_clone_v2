#!/usr/bin/python3
"""
Unit tests for the State class
"""
import unittest
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """
    Test cases for the State model class.
    """

    def setUp(self):
        """
        Simple setup before each test method.
        """
        self.state_instance = State()

    def test_inheritance(self):
        """
        Test if the instance is an instance of BaseModel and State
        """
        self.assertIsInstance(self.state_instance, State)
        self.assertIsInstance(self.state_instance, BaseModel)

    def test_attributes(self):
        """
        Test if State has the correct attributes and if they are set correctly
        """
        self.assertTrue(hasattr(State, "name"),
                        "State class does not have attribute 'name'")
        self.assertIsInstance(State.name, str)

    def test_name_assignment(self):
        """
        Test assignment and type of 'name' attribute.
        """
        self.state_instance.name = "California"
        self.assertEqual(self.state_instance.name, "California")
        self.assertIsInstance(self.state_instance.name, str)

    def tearDown(self):
        """
        Clean up actions after each test method.
        """
        del self.state_instance


if __name__ == '__main__':
    unittest.main()
