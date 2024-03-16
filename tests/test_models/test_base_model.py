#!/usr/bin/python3
"""Module to test BaseModel functionality."""
import unittest
import os
from models import storage
from models.base_model import BaseModel
import datetime
from uuid import UUID
import json

class TestBaseModelFileStorage(unittest.TestCase):
    """Class to test BaseModel with FileStorage."""
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'Skipping test for DB storage')
    def setUp(self):
        """Set up test environment before each test."""
        self.model = BaseModel()
        self.model.save()

    def tearDown(self):
        """Clean up files after each test."""
        try:
            os.remove('file.json')
        except Exception:
            pass

class TestBaseModel(unittest.TestCase):
    """Class for testing BaseModel methods."""

    def setUp(self):
        """Set up test methods."""
        pass

    def tearDown(self):
        """Clean up after test."""
        try:
            os.remove('file.json')
        except:
            pass

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
        key = "BaseModel." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ """
        i = self.value()
        self.assertEqual(str(i), '[BaseModel] ({}) {}'.format(i.id, i.__dict__))

    def test_todict(self):
        """ """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = BaseModel(**n)

    def test_kwargs_one(self):
        """ """
        n = {'Name': 'test'}
        with self.assertRaises(KeyError):
            new = BaseModel(**n)

    def test_id(self):
        """ """
        new = BaseModel()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = BaseModel()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ """
        new = BaseModel()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

if __name__ == "__main__":
    unittest.main()
