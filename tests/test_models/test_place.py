#!/usr/bin/python3
"""
A unit testing module for the Place class.
"""
from tests.test_models.test_base_model import test_basemodel
from models.place import Place

class TestPlaceAttributes(test_basemodel):
    """
    Tests for ensuring the attributes of the Place class are correctly typed.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the test case with Place-specific parameters.
        """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_attribute_city_id(self):
        """
        Validates the type of the 'city_id' attribute.
        """
        instance = self.value()
        self.assertIs(type(instance.city_id), str)

    def test_attribute_user_id(self):
        """
        Validates the type of the 'user_id' attribute.
        """
        instance = self.value()
        self.assertIs(type(instance.user_id), str)

    def test_attribute_name(self):
        """
        Validates the type of the 'name' attribute.
        """
        instance = self.value()
        self.assertIs(type(instance.name), str)

    def test_attribute_description(self):
        """
        Validates the type of the 'description' attribute.
        """
        instance = self.value()
        self.assertIs(type(instance.description), str)

    def test_attribute_number_rooms(self):
        """
        Validates the type of the 'number_rooms' attribute.
        """
        instance = self.value()
        self.assertIs(type(instance.number_rooms), int)

    def test_attribute_number_bathrooms(self):
        """
        Validates the type of the 'number_bathrooms' attribute.
        """
        instance = self.value()
        self.assertIs(type(instance.number_bathrooms), int)

    def test_attribute_max_guest(self):
        """
        Validates the type of the 'max_guest' attribute.
        """
        instance = self.value()
        self.assertIs(type(instance.max_guest), int)

    def test_attribute_price_by_night(self):
        """
        Validates the type of the 'price_by_night' attribute.
        """
        instance = self.value()
        self.assertIs(type(instance.price_by_night), int)

    def test_attribute_latitude(self):
        """
        Validates the type of the 'latitude' attribute.
        """
        instance = self.value()
        self.assertIs(type(instance.latitude), float)

    def test_attribute_longitude(self):
        """
        Validates the type of the 'longitude' attribute.
        """
        instance = self.value()
        self.assertIs(type(instance.longitude), float)

    def test_attribute_amenity_ids(self):
        """
        Validates the type of the 'amenity_ids' attribute.
        """
        instance = self.value()
        self.assertIs(type(instance.amenity_ids), list)
