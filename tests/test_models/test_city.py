#!/usr/bin/python3
"""
Unit tests for the City class.
"""
import unittest
from models.base_model import BaseModel
from models.city import City


class TestCity(unittest.TestCase):
    """Define tests for the City class."""

    def setUp(self):
        """
        Create a new instance of City before each test.
        """
        self.city = City()

    def tearDown(self):
        """
        Delete the City instance before the next test.
        """
        del self.city

    def test_inheritance(self):
        """
        Test if City is a subclass of BaseModel.
        """
        self.assertTrue(issubclass(City, BaseModel))

    def test_attributes(self):
        """
        Test for attributes in the City class.
        """
        self.assertTrue(hasattr(City, "state_id"))
        self.assertTrue(hasattr(City, "name"))

    def test_type_state_id(self):
        """
        Test the type of state_id.
        """
        self.assertIsInstance(self.city.state_id, str)

    def test_type_name(self):
        """
        Test the type of name.
        """
        self.assertIsInstance(self.city.name, str)

    def test_creation_with_kwargs(self):
        """
        Test creating a City instance with keyword arguments.
        """
        kwargs = {"state_id": "State.1234", "name": "San Francisco"}
        city = City(**kwargs)
        for key, value in kwargs.items():
            self.assertEqual(getattr(city, key), value)

    def test_str_representation(self):
        """
        Test the string representation of the City instance.
        """
        self.city.name = "Test City"
        self.city.state_id = "State.1234"
        str_format = "[City] ({}) {}".format(self.city.id, self.city.__dict__)
        self.assertEqual(str(self.city), str_format)


if __name__ == "__main__":
    unittest.main()
