#!/usr/bin/python3
import unittest
from models.amenity import Amenity

class TestAmenity(unittest.TestCase):
    """Tests for the Amenity class."""
    def setUp(self):
        """Set up test methods."""
        self.amenity_instance = Amenity()
        self.amenity_instance.name = "Wi-Fi"

    def test_attributes(self):
        """Test the attributes of Amenity instances."""
        self.assertEqual(self.amenity_instance.name, "Wi-Fi")
        self.assertTrue(hasattr(self.amenity_instance, "id"))
        self.assertTrue(hasattr(self.amenity_instance, "created_at"))
        self.assertTrue(hasattr(self.amenity_instance, "updated_at"))

if __name__ == "__main__":
    unittest.main()
