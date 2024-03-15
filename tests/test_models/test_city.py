#!/usr/bin/python3
import unittest
from models.city import City

class TestCity(unittest.TestCase):
    """Tests for the City class."""
    def setUp(self):
        """Set up test methods."""
        self.city_instance = City()
        self.city_instance.name = "San Francisco"
        self.city_instance.state_id = "CA"

    def test_attributes(self):
        """Test the attributes of City instances."""
        self.assertEqual(self.city_instance.name, "San Francisco")
        self.assertEqual(self.city_instance.state_id, "CA")
        self.assertTrue(hasattr(self.city_instance, "id"))
        self.assertTrue(hasattr(self.city_instance, "created_at"))
        self.assertTrue(hasattr(self.city_instance, "updated_at"))

if __name__ == "__main__":
    unittest.main()
