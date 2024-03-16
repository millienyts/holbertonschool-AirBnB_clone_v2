#!/usr/bin/python3
"""
Unit tests for the FileStorage class in the models.engine package.
"""

import unittest
import os
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

class FileStorageTestCase(unittest.TestCase):
    """
    Defines test cases for the FileStorage class functionality.
    """

    def setUp(self):
        """
        Prepares the environment before each test: creates instances
        and setups necessary variables.
        """
        self.file_storage_instance = FileStorage()
        self.sample_model = BaseModel()

    def tearDown(self):
        """
        Clean up actions after each test: removes the storage file if it exists.
        """
        try:
            os.unlink("file.json")
        except OSError:
            pass

    def test_return_type_of_all_method(self):
        """
        Verifies if the 'all' method returns a dictionary.
        """
        all_objects = self.file_storage_instance.all()
        self.assertTrue(isinstance(all_objects, dict))

    def test_new_method_updates_objects(self):
        """
        Ensures the 'new' method correctly adds objects to the storage.
        """
        self.file_storage_instance.new(self.sample_model)
        object_key = f"{type(self.sample_model).__name__}.{self.sample_model.id}"
        self.assertIn(object_key, self.file_storage_instance._FileStorage__objects)

    def test_value_type_in_objects_dict(self):
        """
        Checks if the stored values in the objects dictionary are instances
        of the correct class.
        """
        self.file_storage_instance.new(self.sample_model)
        object_key = f"{type(self.sample_model).__name__}.{self.sample_model.id}"
        stored_object = self.file_storage_instance._FileStorage__objects[object_key]
        self.assertEqual(type(self.sample_model), type(stored_object))

    def test_file_creation_on_save(self):
        """
        Tests if the 'save' method actually creates the 'file.json'.
        """
        self.file_storage_instance.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_content_type_in_saved_file(self):
        """
        Verifies the content and type of data stored in 'file.json'.
        """
        self.file_storage_instance.new(self.sample_model)
        self.file_storage_instance.save()

        with open("file.json", "r", encoding="utf-8") as file:
            contents = json.load(file)
            self.assertTrue(isinstance(contents, dict))

        with open("file.json", "r", encoding="utf-8") as file:
            contents = file.read()
            self.assertTrue(isinstance(contents, str))

    def test_reload_method_with_no_file(self):
        """
        Confirms that calling 'reload' without an existing 'file.json'
        doesn't raise any exceptions.
        """
        try:
            self.file_storage_instance.reload()
            executed_without_issues = True
        except Exception:
            executed_without_issues = False

        self.assertTrue(executed_without_issues)
      def test_filestorage_base_model_integration(self):
            """
            Tests if BaseModel instances can be correctly serialized and saved to file.json,
            then deserialized back into objects.
            """
            self.sample_model.save()
            self.file_storage_instance.reload()
            all_objects = self.file_storage_instance.all()
            self.assertIn(f"BaseModel.{self.sample_model.id}", all_objects)

        def test_filestorage_user_integration(self):
            """
            Tests if User instances can be correctly serialized and saved to file.json,
            then deserialized back into objects.
            """
            self.sample_user.save()
            self.file_storage_instance.reload()
            all_objects = self.file_storage_instance.all()
            self.assertIn(f"User.{self.sample_user.id}", all_objects)

        def test_save_updates_file(self):
            """
            Tests if calling save on FileStorage instance updates the file.json as expected.
            """
            initial_count = os.path.getsize("file.json") if os.path.exists("file.json") else 0
            self.sample_model.save()
            updated_count = os.path.getsize("file.json")
            self.assertGreater(updated_count, initial_count, "File size should increase after saving.")

    if __name__ == "__main__":
        unittest.main()
