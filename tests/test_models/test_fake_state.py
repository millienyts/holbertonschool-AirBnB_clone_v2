#!/usr/bin/python3
import unittest
from models.state import State
from datetime import datetime

class TestState(unittest.TestCase):
    """Tests for the State class."""

    def setUp(self):
        """Set up test methods."""
        self.state_instance = State()
        self.state_instance.name = "California"

    def test_instance_creation(self):
        """Test instance creation and attribute assignment."""
        self.assertTrue(isinstance(self.state_instance, State))
        self.assertEqual(self.state_instance.name, "California")

    def test_inheritance(self):
        """Test that State class correctly inherits from BaseModel."""
        self.assertTrue(hasattr(self.state_instance, "id"))
        self.assertTrue(hasattr(self.state_instance, "created_at"))
        self.assertTrue(hasattr(self.state_instance, "updated_at"))
        self.assertTrue(isinstance(self.state_instance.created_at, datetime))
        self.assertTrue(isinstance(self.state_instance.updated_at, datetime))

    def test_save_method(self):
        """Test the save method."""
        old_updated_at = self.state_instance.updated_at
        self.state_instance.save()
        self.assertNotEqual(self.state_instance.updated_at, old_updated_at)

    def test_to_dict_method(self):
        """Test conversion of object attributes to dictionary for json."""
        state_dict = self.state_instance.to_dict()
        self.assertEqual(state_dict["__class__"], "State")
        self.assertEqual(state_dict["name"], "California")
        self.assertTrue("created_at" in state_dict)
        self.assertTrue("updated_at" in state_dict)
        self.assertTrue("id" in state_dict)

if __name__ == "__main__":
    unittest.main()

