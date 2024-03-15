#!/usr/bin/python3
"""test for BaseModel"""
import unittest
import os
import pep8
from models import storage
from models.base_model import BaseModel
from datetime import datetime
import json

class TestBaseModel(unittest.TestCase):
    """this will test the base model class"""

    @classmethod
    def setUpClass(cls):
        """setup for the test"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        storage.delete_all()
        cls.base = BaseModel()

    @classmethod
    def tearDownClass(cls):
        """at the end of the test this will tear it down"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.base

    def setUp(self):
        """Set up test methods."""
        pass

    def tearDown(self):
        """Clean up test methods."""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_pep8_BaseModel(self):
        """Testing for pep8"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/base_model.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_BaseModel(self):
        """Checking for docstrings"""
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.__init__.__doc__)
        self.assertIsNotNone(BaseModel.__str__.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)
        self.assertIsNotNone(BaseModel.delete.__doc__)

    def test_method_BaseModel(self):
        """Checking if BaseModel has methods"""
        self.assertTrue(hasattr(BaseModel, "__init__"))
        self.assertTrue(hasattr(BaseModel, "save"))
        self.assertTrue(hasattr(BaseModel, "to_dict"))
        self.assertTrue(hasattr(BaseModel, "__str__"))
        self.assertTrue(hasattr(BaseModel, "delete"))

    def test_init_BaseModel(self):
        """Test if the base is an instance of BaseModel"""
        self.assertTrue(isinstance(self.base, BaseModel))

    def test_kwargs(self):
        """Test initialization with kwargs."""
        date = datetime.utcnow()
        base = BaseModel(id="3", created_at=date.isoformat())
        self.assertEqual(base.id, "3")
        self.assertEqual(base.created_at, date)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == 'db', "skip if database storage")
    def test_save_BaseModel(self):
        """Test if the save works"""
        prev = self.base.updated_at
        self.base.save()
        self.assertLess(prev, self.base.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("BaseModel.{}".format(self.base.id), f.read())
        self.assertNotEqual(self.base.created_at, self.base.updated_at)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == 'db', "skip if database storage")
    def test_delete(self):
        """Test delete method."""
        self.base.delete()
        self.assertNotIn(self.base, storage.all().values())

    def test_to_dict_BaseModel(self):
        """Test if dictionary works"""
        base_dict = self.base.to_dict()
        self.assertEqual(self.base.__class__.__name__, 'BaseModel')
        self.assertIsInstance(base_dict['created_at'], str)
        self.assertIsInstance(base_dict['updated_at'], str)

    def test_id(self):
        """Test id property."""
        self.assertEqual(type(self.base.id), str)

    def test_created_at(self):
        """Test created_at property."""
        self.assertEqual(type(self.base.created_at), datetime)

    def test_updated_at(self):
        """Test updated_at property."""
        self.assertEqual(type(self.base.updated_at), datetime)

if __name__ == "__main__":
    unittest.main()
