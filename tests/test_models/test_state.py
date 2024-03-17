#!/usr/bin/python3
""" """
import unittest
import os
from models import storage
from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)
        
        @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'Skipping test for DB storage')
class TestStateFileStorage(unittest.TestCase):
    # Your State model test methods for FileStorage here
    pass
