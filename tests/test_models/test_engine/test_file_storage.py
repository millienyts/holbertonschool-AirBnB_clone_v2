#!/usr/bin/python3
"""
Module for testing file storage.
Combines tests for FileStorage methods, including setup and teardown, 
functionality tests, and command line interface interaction via the HBNBCommand class.
"""
import unittest
from models.base_model import BaseModel
from models import storage
from console import HBNBCommand
import os
from unittest.mock import patch
from io import StringIO

class TestFileStorage(unittest.TestCase):
    """
    Class to test the file storage method, including both direct method invocation
    and command line interface interaction.
    """

    def setUp(self):
        """
        Set up the test environment by clearing the storage object dictionary.
        """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """
        Clean up after tests by removing the storage file.
        """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_obj_list_empty(self):
        """
        Test that the storage objects list is initially empty.
        """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """
        Test that a new object is correctly added to the storage.
        """
        new = BaseModel()
        self.assertIn(f"BaseModel.{new.id}", storage.all())

    def test_all(self):
        """
        Test that the all method correctly returns the storage objects dictionary.
        """
        new = BaseModel()
        self.assertIsInstance(storage.all(), dict)

    def test_base_model_instantiation(self):
        """
        Test that a file is not unnecessarily created upon BaseModel instantiation.
        """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """
        Test that data is saved to the file.
        """
        new = BaseModel()
        new.save()
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """
        Test the FileStorage save method.
        """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """
        Test that the storage file is successfully loaded into the objects dictionary.
        """
        new = BaseModel()
        new.save()
        storage.reload()
        self.assertIn(f"BaseModel.{new.id}", storage.all())

    def test_reload_empty(self):
        """
        Test that attempting to load from an empty file raises a ValueError.
        """
        with open('file.json', 'w'):
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """
        Test that attempting to reload from a nonexistent file does nothing harmful.
        """
        self.assertIsNone(storage.reload())

    def test_base_model_save(self):
        """
        Test that the BaseModel save method triggers the storage save method.
        """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """
        Test that the file path is stored as a string.
        """
        self.assertIsInstance(storage._FileStorage__file_path, str)

    def test_type_objects(self):
        """
        Test that the objects are stored in a dictionary.
        """
        self.assertIsInstance(storage.all(), dict)

    def test_key_format(self):
        """
        Test that keys in the storage dictionary are correctly formatted.
        """
        new = BaseModel()
        expected_key = f"BaseModel.{new.id}"
        self.assertIn(expected_key, storage.all())

    def test_storage_var_created(self):
        """
        Test that the FileStorage object is correctly instantiated.
        """
        from models.engine.file_storage import FileStorage
        self.assertIsInstance(storage, FileStorage)

    def test_do_create_with_parameters(self):
        """
        Test creating an object via the console with initial parameters.
        """
        with patch('sys.stdout', new_callable=StringIO) as mocked_stdout:
            command = 'create BaseModel name="Test" number=100'
            HBNBCommand().onecmd(command)
            obj_id = mocked_stdout.getvalue().strip()
            self.assertTrue(obj_id)

            obj_key = f"BaseModel.{obj_id}"
            self.assertIn(obj_key, storage.all())

            obj = storage.all()[obj_key]
            self.assertEqual(obj.name, "Test")
            self.assertEqual(obj.number, 100)

if __name__ == "__main__":
    unittest.main()
