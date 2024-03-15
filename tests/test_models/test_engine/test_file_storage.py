#!/usr/bin/python3
import os
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel

class TestFileStorage(unittest.TestCase):
    """Defines enhanced tests for FileStorage class including new functionalities."""

    def setUp(self):
        """Prepares the test environment before each test."""
        self.storage = FileStorage()
        self.file_path = FileStorage._FileStorage__file_path
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_save_and_reload(self):
        """Tests saving objects to file and reloading them."""
        obj = BaseModel()
        obj.name = "Holberton"
        obj.my_number = 89
        self.storage.new(obj)
        self.storage.save()

        new_storage = FileStorage()
        new_storage.reload()

        objects = new_storage.all()
        self.assertIn(f"BaseModel.{obj.id}", objects)
        reloaded_obj = objects[f"BaseModel.{obj.id}"]
        self.assertEqual(reloaded_obj.name, "Holberton")
        self.assertEqual(reloaded_obj.my_number, 89)

    def test_all_method_returns_all_objects(self):
        """Tests that all() method returns all stored objects."""
        initial_count = len(self.storage.all())
        obj = BaseModel()
        self.storage.new(obj)
        self.assertEqual(len(self.storage.all()), initial_count + 1)

    def test_new_method_adds_objects(self):
        """Tests that new() correctly adds objects."""
        obj = BaseModel()
        self.storage.new(obj)
        self.assertIn(f"BaseModel.{obj.id}", self.storage.all())

    def test_save_creates_and_updates_file(self):
        """Tests that save() method creates and updates the storage file."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))

    def test_reload_method(self):
        """Tests reloading objects from the storage file."""
        obj = BaseModel()
        obj.name = "Reload Test"
        self.storage.new(obj)
        self.storage.save()

        new_storage = FileStorage()
        new_storage.reload()

        objects = new_storage.all()
        self.assertIn(f"BaseModel.{obj.id}", objects)
        self.assertEqual(objects[f"BaseModel.{obj.id}"].name, "Reload Test")

    def test_no_argument_behavior(self):
        """Tests methods behavior with no arguments where applicable."""
        with self.assertRaises(TypeError):
            self.storage.save("unnecessary argument")  # save should not accept arguments

        # Additional no argument tests for methods like `new()` or `all()` can be added based on second code insights

    def tearDown(self):
        """Cleans up after each test."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

if __name__ == "__main__":
    unittest.main()
