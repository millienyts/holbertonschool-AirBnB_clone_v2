"""
Tests for the State model and its documentation.
"""

from datetime import datetime
import inspect
import models
from models import state
from models.base_model import BaseModel
import pycodestyle
import unittest
State = state.State

class TestStateDocs(unittest.TestCase):
    """Tests to ensure documentation and style compliance for the State class."""

    @classmethod
    def setUpClass(cls):
        """Prepare for testing documentation and style."""
        cls.state_funcs = inspect.getmembers(State, inspect.isfunction)

    def test_pycodestyle_conformance_state(self):
        """Check that models/state.py adheres to Pycodestyle."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0, "Code style issues found.")

    def test_pycodestyle_conformance_test_state(self):
        """Ensure tests for state model conform to Pycodestyle."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_state.py'])
        self.assertEqual(result.total_errors, 0, "Code style issues found in tests.")

    def test_state_module_docstring(self):
        """Validate docstring presence in the state module."""
        self.assertIsNotNone(state.__doc__, "Missing docstring in state module.")

    def test_state_class_docstring(self):
        """Ensure the State class has a docstring."""
        self.assertIsNotNone(State.__doc__, "Missing docstring in the State class.")

    def test_state_func_docstrings(self):
        """Check for docstrings in all functions of the State class."""
        for function in self.state_funcs:
            self.assertIsNotNone(function[1].__doc__, f"Missing docstring in the function {function[0]}.")

class TestState(unittest.TestCase):
    """Validate functionality of the State class."""

    def test_is_subclass(self):
        """Confirm that State is a subclass of BaseModel."""
        state_instance = State()
        self.assertIsInstance(state_instance, BaseModel)

    def test_name_attribute(self):
        """Test the type of the name attribute."""
        state_instance = State()
        self.assertIsInstance(state_instance.name, (str, type(None)))

    def test_to_dict_method(self):
        """Check the dictionary representation of a State instance."""
        state_instance = State()
        state_dict = state_instance.to_dict()
        self.assertIsInstance(state_dict, dict)
        self.assertTrue('__class__' in state_dict)

    def test_values_in_dict(self):
        """Ensure values in the dict returned from to_dict are accurate."""
        state_instance = State()
        state_dict = state_instance.to_dict()
        expected_attrs = ["id", "created_at", "updated_at", "__class__", "name"]
        self.assertCountEqual(state_dict.keys(), expected_attrs)

    def test_str_representation(self):
        """Verify the string representation of State instances."""
        state_instance = State()
        expected_format = f"[State] ({state_instance.id}) {state_instance.__dict__}"
        self.assertEqual(str(state_instance), expected_format)

if __name__ == "__main__":
    unittest.main()
