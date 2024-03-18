#!/usr/bin/python3
"""
A module for testing the City class.
"""
from tests.test_models.test_base_model import test_basemodel
from models.city import City
import pycodestyle
import unittest
import os
from models.base_model import BaseModel

class TestCityInheritance(test_basemodel):
    """
    Tests the City class for inheritance from BaseModel and attribute assignments.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the test case for the City class.
        """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id_attr(self):
        """
        Tests the state_id attribute of the City class.
        """
        new_city = self.value()
        self.assertEqual(type(new_city.state_id), str)

    def test_name_attr(self):
        """
        Tests the name attribute of the City class.
        """
        new_city = self.value()
        self.assertEqual(type(new_city.name), str)

class TestCityPEP8Compliance(unittest.TestCase):
    """
    Tests the PEP 8 compliance of the city.py file.
    """

    def test_pep8_conformance(self):
        """
        Checks if the city.py file conforms to PEP 8 standards.
        """
        pep8_style = pycodestyle.StyleGuide(quiet=True)
        result = pep8_style.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0, "Detected code style errors and warnings.")

class TestCityFeatures(unittest.TestCase):
    """
    Tests specific features and functionalities of the City class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup for the City class tests.
        """
        cls.test_city = City()
        cls.test_city.name = "Los Angeles"
        cls.test_city.state_id = "CA"

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests have run.
        """
        del cls.test_city

    def tearDown(self):
        """
        Clean up after each test method.
        """
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_pep8_compliance(self):
        """
        Test that the city.py file is fully PEP 8 compliant.
        """
        pep8_check = pycodestyle.StyleGuide(quiet=True)
        result = pep8_check.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0, "PEP 8 issues found.")

    def test_docstrings_existence(self):
        """
        Test for the presence of docstrings in the City class.
        """
        self.assertIsNotNone(City.__doc__)

    def test_city_attributes_existence(self):
        """
        Checks that the City instance has the required attributes.
        """
        self.assertTrue(hasattr(self.test_city, 'id'))
        self.assertTrue(hasattr(self.test_city, 'created_at'))
        self.assertTrue(hasattr(self.test_city, 'updated_at'))
        self.assertTrue(hasattr(self.test_city, 'state_id'))
        self.assertTrue(hasattr(self.test_city, 'name'))

    def test_city_is_subclass_of_base_model(self):
        """
        Verifies that City is a subclass of BaseModel.
        """
        self.assertTrue(issubclass(type(self.test_city), BaseModel))

    def test_city_attributes_types(self):
        """
        Checks the types of City class attributes.
        """
        self.assertIsInstance(self.test_city.name, str)
        self.assertIsInstance(self.test_city.state_id, str)

    def test_city_save_method(self):
        """
        Tests the 'save' method of the City class.
        """
        self.test_city.save()
        self.assertNotEqual(self.test_city.created_at, self.test_city.updated_at)

    def test_city_to_dict_method(self):
        """
        Tests the 'to_dict' method of the City class.
        """
        self.assertTrue(callable(getattr(self.test_city, "to_dict", None)))

if __name__ == "__main__":
    unittest.main()
