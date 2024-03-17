"""Unit tests for the User class in the AirBnB clone project."""

from tests.test_models.test_base_model import test_basemodel
from models.user import User
import unittest

class TestUser(test_basemodel):
    """Tests for the User model attributes and functionality."""

    def __init__(self, *args, **kwargs):
        """Initialize the test case with User-specific setup."""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name_attribute(self):
        """Test that the User model has a first name attribute of type str."""
        user_instance = self.value()
        self.assertIsInstance(user_instance.first_name, str, msg="first_name is not a string")

    def test_last_name_attribute(self):
        """Test that the User model has a last name attribute of type str."""
        user_instance = self.value()
        self.assertIsInstance(user_instance.last_name, str, msg="last_name is not a string")

    def test_email_attribute(self):
        """Test that the User model has an email attribute of type str."""
        user_instance = self.value()
        self.assertIsInstance(user_instance.email, str, msg="email is not a string")

    def test_password_attribute(self):
        """Test that the User model has a password attribute of type str."""
        user_instance = self.value()
        self.assertIsInstance(user_instance.password, str, msg="password is not a string")

if __name__ == "__main__":
    unittest.main()
