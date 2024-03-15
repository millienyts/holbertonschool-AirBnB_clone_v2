#!/usr/bin/python3
"""FileStorage class testing."""
import unittest
import pep8
import json
import os
from models import (BaseModel, User, State, City, Amenity, Place, Review, 
                    engine)
from models.engine.file_storage import FileStorage

class FileStorageTestCase(unittest.TestCase):
    '''Series of tests for the FileStorage class.'''

    @classmethod
    def setUpClass(cls):
        """Setting up the test scenario before all tests."""

        try:
            os.rename("file.json", "backup_file.json")
        except Exception:
            pass
        cls.test_storage = FileStorage()
        cls.initial_setup()

    @classmethod
    def tearDownClass(cls):
        """Cleaning up after running all tests."""
        try:
            os.remove("file.json")
        except Exception:
            pass
        try:
            os.rename("backup_file.json", "file.json")
        except Exception:
            pass

    @classmethod
    def initial_setup(cls):
        """Initial setup for tests in the class."""
        cls.entities = {
            'BaseModel': BaseModel(), 'User': User(), 'State': State(),
            'City': City(), 'Amenity': Amenity(), 'Place': Place(),
            'Review': Review()
        }
        for entity_name, entity_obj in cls.entities.items():
            cls.test_storage.new(entity_obj)

    def setUp(self):
        """Runs before each test."""
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Runs after each test."""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_compliance(self):
        """PEP8 compliance for file_storage.py."""
        pep8_style = pep8.StyleGuide(quiet=True)
        result = pep8_style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0, "Code should be PEP8 compliant.")

    def test_file_storage_all_method(self):
        """Verify 'all' method functionality."""
        all_objs = self.test_storage.all()
        self.assertIsInstance(all_objs, dict, "Should return a dictionary.")

    def test_file_storage_new_method(self):
        """Check 'new' method functionality."""
        for entity_obj in self.entities.values():
            self.assertIn(entity_obj, self.test_storage.all().values())

    def test_file_storage_reload_method(self):
        """Test reloading from the file."""
        self.test_storage.reload()
        self.assertTrue(len(self.test_storage.all()) > 0, "Reload should populate the storage.")

    def test_file_storage_save_method(self):
        """Test saving to the file."""
        initial_count = len(self.test_storage.all())
        new_model = BaseModel()
        self.test_storage.new(new_model)
        self.test_storage.save()
        self.test_storage.reload()
        final_count = len(self.test_storage.all())
        self.assertNotEqual(initial_count, final_count, "New object should be saved to the file.")

if __name__ == '__main__':
    unittest.main()
