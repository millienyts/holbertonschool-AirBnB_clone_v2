"""
Unit tests for the FileStorage class in the AirBnB clone project.
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pycodestyle
import unittest
FileStorage = file_storage.FileStorage

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

class TestFileStorageDocs(unittest.TestCase):
    """Verifies that the FileStorage class and its methods are documented and follow PEP8."""

    @classmethod
    def setUpClass(cls):
        """Gathers all the functions in FileStorage for inspection."""
        cls.fs_functions = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pycodestyle_conformance_file_storage(self):
        """Ensures models/engine/file_storage.py adheres to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0, "Found style issues.")

    def test_pycodestyle_conformance_test_file_storage(self):
        """Checks tests for file_storage.py for PEP8 compliance."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_engine/test_file_storage.py'])
        self.assertEqual(result.total_errors, 0, "Found style issues in tests.")

    def test_file_storage_module_docstring(self):
        """Tests the presence of a module docstring in file_storage.py."""
        self.assertIsNotNone(file_storage.__doc__, "Module docstring missing.")

    def test_file_storage_class_docstring(self):
        """Verifies the FileStorage class has a docstring."""
        self.assertIsNotNone(FileStorage.__doc__, "Class docstring missing.")

    def test_fs_function_docstrings(self):
        """Confirms all methods in FileStorage have docstrings."""
        for func in self.fs_functions:
            self.assertIsNotNone(func[1].__doc__, f"{func[0]} lacks a docstring.")

class TestFileStorageFunctionality(unittest.TestCase):
    """Tests specific functionalities of the FileStorage class."""

    @unittest.skipIf(models.storage_t == 'db', "Skipping FileStorage tests under db storage")
    def test_all_returns_dict(self):
        """Confirms all() returns a dict of __objects."""
        self.assertIsInstance(models.storage.all(), dict, "all() should return a dict.")

    @unittest.skipIf(models.storage_t == 'db', "Skipping FileStorage tests under db storage")
    def test_new_method(self):
        """Validates that new() adds objects correctly."""
        original = FileStorage._FileStorage__objects.copy()
        try:
            test_obj = list(classes.values())[0]()
            models.storage.new(test_obj)
            self.assertIn(f"{type(test_obj).__name__}.{test_obj.id}", models.storage.all())
        finally:
            FileStorage._FileStorage__objects = original

    @unittest.skipIf(models.storage_t == 'db', "Skipping FileStorage tests under db storage")
    def test_save_to_file(self):
        """Checks that save() method serializes to file.json correctly."""
        original = FileStorage._FileStorage__objects.copy()
        try:
            models.storage.save()
            path = FileStorage._FileStorage__file_path
            self.assertTrue(os.path.exists(path), "file.json was not created.")
        finally:
            FileStorage._FileStorage__objects = original

if __name__ == "__main__":
    unittest.main()
