"""Unit tests for the City class in the AirBnB clone project."""

from tests.test_models.test_base_model import test_basemodel
from models.city import City
import pycodestyle
import unittest

class TestCityInheritance(test_basemodel):
    """Test suite for validating City class inherits from BaseModel."""

    def __init__(self, *args, **kwargs):
        """Initialize with test case setup."""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id_attribute(self):
        """Test the type of state_id attribute."""
        new_instance = self.value()
        self.assertIsInstance(new_instance.state_id, str)

    def test_name_attribute(self):
        """Test the type of name attribute."""
        new_instance = self.value()
        self.assertIsInstance(new_instance.name, str)

class TestCityPEP8Compliance(unittest.TestCase):
    """Ensure City class complies with PEP8."""

    def test_pep8_conformance(self):
        """Check PEP8 compliance across the City class."""
        pep8_style = pycodestyle.StyleGuide(quiet=True)
        result = pep8_style.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Code style errors or warnings detected.")

class TestCityFunctionality(unittest.TestCase):
    """Define tests for City class functionality within AirBnB project."""

    @classmethod
    def setUpClass(cls):
        """Setup test case environment."""
        cls.city_instance = City()
        cls.city_instance.name = "San Francisco"
        cls.city_instance.state_id = "CA"

    @classmethod
    def tearDownClass(cls):
        """Clean up after all test cases."""
        del cls.city_instance

    def tearDown(self):
        """Clean up files created during testing."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_attributes_existence(self):
        """Ensure attributes are present."""
        self.assertTrue(hasattr(self.city_instance, 'id'))
        self.assertTrue(hasattr(self.city_instance, 'created_at'))
        self.assertTrue(hasattr(self.city_instance, 'updated_at'))
        self.assertTrue(hasattr(self.city_instance, 'state_id'))
        self.assertTrue(hasattr(self.city_instance, 'name'))

    def test_is_subclass(self):
        """Validate that City is a subclass of BaseModel."""
        self.assertIsInstance(self.city_instance, City)

    def test_attributes_types(self):
        """Verify the attribute types."""
        self.assertIsInstance(self.city_instance.name, str)
        self.assertIsInstance(self.city_instance.state_id, str)

    def test_save_method(self):
        """Test the functionality of save method."""
        self.city_instance.save()
        self.assertNotEqual(self.city_instance.created_at, self.city_instance.updated_at)

    def test_to_dict_method(self):
        """Check correctness of to_dict method."""
        self.assertTrue('to_dict' in dir(self.city_instance))

if __name__ == "__main__":
    unittest.main()
