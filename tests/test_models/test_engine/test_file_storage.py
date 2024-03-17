#!/usr/bin/python3
"""
Test Suite for validating the FileStorage mechanism.
Ensures all operations on the JSON storage file work as expected.
"""
import unittest
from models import storage
from models.base_model import BaseModel
import os

class TestFileStorage(unittest.TestCase):
    """Defines tests for FileStorage functionality."""

    def setUp(self):
        """Prepares the environment before each test."""
        self.clean_storage()

    def tearDown(self):
        """Cleans up after tests."""
        try:
            os.unlink('file.json')
        except OSError:
            pass
        self.clean_storage()

    def clean_storage(self):
        """Utility method to clear FileStorage objects."""
        keys_to_delete = list(storage._FileStorage__objects.keys())
        for key in keys_to_delete:
            del storage._FileStorage__objects[key]

    def test_storage_initially_empty(self):
        """Checks if storage is empty at the start."""
        self.assertEqual(len(storage.all()), 0, "Storage should initially be empty.")

    def test_add_new_object(self):
        """Tests adding new objects to storage."""
        instance = BaseModel()
        self.assertIn(instance, storage.all().values(), "New object should be in storage.")

    def test_retrieving_all_objects(self):
        """Verifies that all objects are correctly retrieved."""
        instance = BaseModel()
        self.assertTrue(isinstance(storage.all(), dict), "Storage.all() should return a dictionary.")

    def test_not_creating_file_on_new_instance(self):
        """Confirms that no file is created upon new instance creation."""
        BaseModel()
        self.assertFalse(os.path.isfile('file.json'), "No file should exist without explicit save.")

    def test_saving_to_file(self):
        """Tests that data can be saved to file."""
        instance = BaseModel()
        instance.save()
        self.assertTrue(os.path.isfile('file.json'), "File should exist after saving.")

    def test_loading_from_file(self):
        """Checks loading objects from file."""
        original = BaseModel()
        original.save()
        storage.reload()
        self.assertIn(f'BaseModel.{original.id}', storage.all().keys(), "Object should be loaded from file.")

    def test_empty_file_loading(self):
        """Tests behavior with an empty file."""
        open('file.json', 'w').close()
        self.assertRaises(ValueError, storage.reload)

    def test_missing_file_loading(self):
        """Verifies behavior when the expected file is missing."""
        if os.path.exists('file.json'):
            os.remove('file.json')
        storage.reload()  # Should not raise any exceptions
        self.assertTrue(True, "Missing file should not cause failure on reload.")

    def test_instance_save_updates_storage(self):
        """Ensures BaseModel.save() triggers storage save."""
        instance = BaseModel()
        instance.save()
        self.assertTrue(os.path.exists('file.json'), "File should exist after instance save.")

    def test_path_type(self):
        """Confirms the storage file path is a string."""
        self.assertIsInstance(storage._FileStorage__file_path, str, "__file_path should be a string.")

    def test_objects_type(self):
        """Ensures storage objects are stored in a dictionary."""
        self.assertIsInstance(storage._FileStorage__objects, dict, "__objects should be a dictionary.")

    def test_key_naming_convention(self):
        """Validates the key naming convention for stored objects."""
        instance = BaseModel()
        expected_key = f'BaseModel.{instance.id}'
        self.assertIn(expected_key, storage.all().keys(), "Key should follow the '<class name>.<id>' pattern.")

    def test_storage_instance(self):
        """Confirms that storage is an instance of FileStorage."""
        self.assertIsInstance(storage, storage.__class__, "Storage should be an instance of its class.")

if __name__ == '__main__':
    unittest.main()
