#!/usr/bin/python3
import unittest
from unittest.mock import patch
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import os

class TestBaseModel(unittest.TestCase):
    """Unit tests for the BaseModel class"""

    def test_init(self):
        """Test initialization of BaseModel instances"""
        model = BaseModel()
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))
        self.assertTrue(hasattr(model, "updated_at"))

    def test_str(self):
        """Test the __str__ method of BaseModel"""
        model = BaseModel()
        expected = f"[BaseModel] ({model.id}) {model.__dict__}"
        self.assertEqual(expected, str(model))

    def test_save(self):
        """Test the save method updates `updated_at` and calls storage.save"""
        model = BaseModel()
        original_updated_at = model.updated_at
        with patch.object(storage, 'save') as mock_save:
            model.save()
            self.assertNotEqual(original_updated_at, model.updated_at)
            mock_save.assert_called_once()

    def test_to_dict(self):
        """Test the to_dict method returns a dictionary with correct keys and formats"""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertTrue("created_at" in model_dict and "updated_at" in model_dict)
        self.assertTrue(isinstance(model_dict["created_at"], str) and isinstance(model_dict["updated_at"], str))

# New test class for FileStorage
class TestFileStorage(unittest.TestCase):
    """Unit tests for the FileStorage class."""

    def setUp(self):
        """Set up before each test."""
        self.storage = FileStorage()
        self.file_path = FileStorage._FileStorage__file_path
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_reload_no_file(self):
        """Test reload does not raise exceptions when no file exists."""
        try:
            self.storage.reload()
            self.assertTrue(True)
        except Exception:
            self.fail("reload() raised an exception when no file exists.")

    def test_reload_with_saved_data(self):
        """Test reload correctly loads objects after save."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()

        self.storage.reload()
        objects = self.storage.all()
        self.assertIn(f"BaseModel.{obj.id}", objects)

    def test_all_method_returns_correct_data(self):
        """Test that all() method returns the correct data after reload."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.storage.reload()

        objects = self.storage.all()
        self.assertIn(f"BaseModel.{obj.id}", objects)
        self.assertEqual(objects[f"BaseModel.{obj.id}"].id, obj.id)

    def tearDown(self):
        """Clean up files."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

if __name__ == "__main__":
    unittest.main()
