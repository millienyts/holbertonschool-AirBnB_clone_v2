#!/usr/bin/python3
""" """
import unittest
import os
from models import storage
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'Skipping test for DB storage')
class TestBaseModelFileStorage(unittest.TestCase):
    """
    Defines test cases for the BaseModel class for interactions with FileStorage.
    """

    def setUp(self):
        """Prepare the test environment before each test."""
        self.file_path = 'file.json'
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def tearDown(self):
        """Clean up the test environment after each test."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_instance_creation(self):
        """Test the creation of a BaseModel instance and its existence in FileStorage."""
        instance = BaseModel()
        instance.save()
        self.assertIn(f'BaseModel.{instance.id}', storage.all().keys())

    def test_default(self):
        """Test the default initialization of a BaseModel instance."""
        instance = BaseModel()
        self.assertEqual(type(instance), BaseModel)

    def test_kwargs(self):
        """Test initialization of a BaseModel instance with kwargs."""
        instance = BaseModel()
        instance_dict = instance.to_dict()
        new_instance = BaseModel(**instance_dict)
        self.assertFalse(new_instance is instance)

    def test_save(self):
        """Test the save method of a BaseModel instance."""
        instance = BaseModel()
        instance.save()
        key = f'BaseModel.{instance.id}'
        with open(self.file_path, 'r') as f:
            json_data = json.load(f)
            self.assertIn(key, json_data.keys())

    def test_str(self):
        """Test the string representation of a BaseModel instance."""
        instance = BaseModel()
        expected_str = f'[BaseModel] ({instance.id}) {instance.__dict__}'
        self.assertEqual(str(instance), expected_str)

    def test_todict(self):
        """Test converting a BaseModel instance to a dictionary."""
        instance = BaseModel()
        instance_dict = instance.to_dict()
        self.assertEqual(instance.to_dict(), instance_dict)

    def test_id(self):
        """Test the type of an instance's id."""
        instance = BaseModel()
        self.assertIsInstance(instance.id, str)

    def test_created_at(self):
        """Test the type of an instance's created_at."""
        instance = BaseModel()
        self.assertIsInstance(instance.created_at, datetime.datetime)

    def test_updated_at(self):
        """Test the type of an instance's updated_at."""
        instance = BaseModel()
        self.assertIsInstance(instance.updated_at, datetime.datetime)

if __name__ == "__main__":
    unittest.main()
