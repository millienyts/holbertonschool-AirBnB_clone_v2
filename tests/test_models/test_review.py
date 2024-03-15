#!/usr/bin/python3
import unittest
from models.review import Review

class TestReview(unittest.TestCase):
    """Tests for the Review class."""
    def setUp(self):
        """Set up test methods."""
        self.review_instance = Review()
        self.review_instance.place_id = "1001"
        self.review_instance.user_id = "1001"
        self.review_instance.text = "Great place!"

    def test_attributes(self):
        """Test the attributes of Review instances."""
        self.assertEqual(self.review_instance.place_id, "1001")
        self.assertEqual(self.review_instance.user_id, "1001")
        self.assertEqual(self.review_instance.text, "Great place!")
        self.assertTrue(hasattr(self.review_instance, "id"))
        self.assertTrue(hasattr(self.review_instance, "created_at"))
        self.assertTrue(hasattr(self.review_instance, "updated_at"))

if __name__ == "__main__":
    unittest.main()
