#!/usr/bin/python3
""" """
import unittest
import os
import datetime
from uuid import UUID
import json
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import pep8

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'Skipping test for DB storage')
class TestBaseModelFileStorage(unittest.TestCase):
    """
    Test cases for the `BaseModel` class with a focus on FileStorage integration.
    """

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.storage = FileStorage()
        cls.instance = BaseModel()

    @classmethod
    def tearDownClass(cls):
        """BaseModel testing teardown.
        Restore original file.json.
        Delete the test BaseModel instance.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.storage
        del cls.instance

    def setUp(self):
        """
        Set up the test case environment by ensuring no 'file.json' exists, to start with a clean slate.
        """
        if os.path.exists('file.json'):
            os.remove('file.json')

    def tearDown(self):
        """
        Clean up after tests by removing 'file.json' if it exists.
        """
        if os.path.exists('file.json'):
            os.remove('file.json')

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/base_model.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.__init__.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)
        self.assertIsNotNone(BaseModel.__str__.__doc__)

    def test_instance_save_to_file(self):
        """
        Test if the instance of `BaseModel` is correctly saved to 'file.json'.
        """
        self.instance.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_instance_load_from_file(self):
        """
        Test if the instance of `BaseModel` can be correctly loaded from 'file.json'.
        """
        self.instance.save()
        storage.reload()
        objects = storage.all()
        key = f"{self.instance.__class__.__name__}.{self.instance.id}"
        self.assertIn(key, objects)

    def test_file_contains_correct_data(self):
        """
        Test if 'file.json' contains the correct data of `BaseModel` instances after saving.
        """
        self.instance.save()
        with open('file.json', 'r') as f:
            contents = json.load(f)
            key = f"{self.instance.__class__.__name__}.{self.instance.id}"
            self.assertIn(key, contents)
            self.assertDictEqual(self.instance.to_dict(), contents[key])
    def test_default(self):
        """ """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ """
        n = {'Name': 'test'}
        with self.assertRaises(KeyError):
            new = self.value(**n)

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)
        
  @unittest.skipIf(os.getenv("HBNB_ENV") is not None, "Testing DBStorage")
    def test_save(self):
        """Test save method."""
        old = self.instance.updated_at
        self.instance.save()
        self.assertLess(old, self.instance.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("BaseModel.{}".format(self.instance.id), f.read())

    @unittest.skipIf(os.getenv("HBNB_ENV") is not None, "Testing DBStorage")
    def test_delete(self):
        """Test delete method."""
        self.instance.delete()
        self.assertNotIn(self.instance, FileStorage._FileStorage__objects)

        # Existing test cases for BaseModel functionalities without FileStorage

class test_basemodel(unittest.TestCase):
    """
    Test cases for `BaseModel` functionalities unrelated to FileStorage.
    """

    def setUp(self):
        """
        Prepare each test case environment.
        """
        self.value = BaseModel()

    def tearDown(self):
        """
        Clean up after each test case.
        """
        pass

    # Examples:
    def test_default(self):
        """
        Test default object instantiation.
        """
        self.assertEqual(type(self.value), BaseModel)
    
    # Additional test methods...

if __name__ == "__main__":
    unittest.main()
