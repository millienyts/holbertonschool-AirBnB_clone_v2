#!/usr/bin/env python3
"""
Unit tests for the BaseModel class in the HBNB project.
"""

from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os
import pycodestyle

class BaseModelTest(unittest.TestCase):
    """
    Defines test cases for the BaseModel class functionality.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the BaseModel test class.
        """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def test_PEP8_conformance(self):
        """
        Test that the code conforms to PEP8.
        """
        pep8style = pycodestyle.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style errors found.")

    def setUp(self):
        """
        Set up resources before each test.
        """
        pass

    def tearDown(self):
        """
        Clean up resources after tests.
        """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_default_behavior(self):
        """
        Test the default instantiation of BaseModel.
        """
        instance = self.value()
        self.assertIsInstance(instance, self.value)

    def test_kwargs_initialization(self):
        """
        Test initialization of BaseModel with kwargs.
        """
        instance = self.value()
        copy = instance.to_dict()
        new_instance = BaseModel(**copy)
        self.assertNotEqual(new_instance, instance)

    def test_kwargs_contains_non_dict_argument(self):
        """
        Test that initializing BaseModel with non-dict kwargs raises TypeError.
        """
        instance = self.value()
        copy = instance.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            BaseModel(**copy)

    def test_save_method(self):
        """
        Test the save method of BaseModel.
        """
        instance = self.value()
        instance.save()
        key = self.name + "." + instance.id
        with open('file.json', 'r') as f:
            json_data = json.load(f)
            self.assertEqual(json_data[key], instance.to_dict())

    def test_string_representation(self):
        """
        Test the string representation of BaseModel.
        """
        instance = self.value()
        expected_format = '[{}] ({}) {}'.format(self.name, instance.id, instance.__dict__)
        self.assertEqual(str(instance), expected_format)

    def test_to_dict_method(self):
        """
        Test the to_dict method of BaseModel.
        """
        instance = self.value()
        self.assertEqual(instance.to_dict(), instance.to_dict())

    def test_kwargs_with_None(self):
        """
        Test initializing BaseModel with None key in kwargs raises TypeError.
        """
        with self.assertRaises(TypeError):
            new = self.value(**{None: None})

    def test_unique_id_for_each_instance(self):
        """
        Test that each BaseModel instance has a unique id.
        """
        instance1 = BaseModel()
        instance2 = BaseModel()
        instance3 = BaseModel()
        self.assertNotEqual(instance1.id, instance2.id)
        self.assertNotEqual(instance1.id, instance3.id)
        self.assertNotEqual(instance2.id, instance3.id)

    def test_created_at_attribute(self):
        """
        Test the created_at attribute of BaseModel.
        """
        new_instance = self.value()
        self.assertIsInstance(new_instance.created_at, datetime.datetime)

    def test_updated_at_attribute(self):
        """
        Test the updated_at attribute of BaseModel.
        """
        new_instance = self.value()
        self.assertIsInstance(new_instance.updated_at, datetime.datetime)
        updated = new_instance.to_dict()
        new_instance = BaseModel(**updated)
        self.assertNotEqual(new_instance.created_at, new_instance.updated_at)

    def test_uuid_is_string(self):
        """
        Test that the id attribute of BaseModel is a string.
        """
        instance = BaseModel()
        self.assertIsInstance(instance.id, str)

    def test_str_magic_method(self):
        """
        Test the __str__ method of BaseModel.
        """
        instance = BaseModel()
        expected_output = "[BaseModel] ({}) {}".format(instance.id, instance.__dict__)
        self.assertEqual(str(instance), expected_output)

class TestPEP8Compliance(unittest.TestCase):
    """
    Test PEP8 compliance of the base_model file.
    """
    def test_pep8(self):
        """
        Ensure the base_model.py file is PEP8 compliant.
        """
        pep8style = pycodestyle.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 issues found.")

class TestDocumentation(unittest.TestCase):
    """
    Test documentation of the BaseModel class and its methods.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up class method for docstring tests.
        """
        cls.obj_members = inspect.getmembers(BaseModel, inspect.isfunction)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after docstring tests.
        """
        del cls.obj_members

    def test_module_docstring(self):
        """
        Test for existence of the module docstring.
        """
        self.assertTrue(len(BaseModel.__doc__) >= 1)

    def test_method_docstrings(self):
        """
        Test for the existence of docstrings in BaseModel methods.
        """
        for method in self.obj_members:
            self.assertTrue(len(method[1].__doc__) >= 1)

if __name__ == "__main__":
    unittest.main()
