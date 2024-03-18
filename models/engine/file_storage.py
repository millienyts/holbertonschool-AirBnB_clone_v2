#!/usr/bin/python3
"""
Defines a class to manage file storage for the HBnB clone project.

This module implements the FileStorage class which serializes instances to a JSON file
and deserializes JSON file to instances. It supports operations such as adding new objects,
saving objects to a file, reloading objects from a file, and deleting objects.
"""

import json

class FileStorage:
    """
    Manages storage of HBnB models in JSON format.

    Attributes:
        __file_path (str): Path to the JSON file used for storage.
        __objects (dict): A dictionary of instantiated objects.
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        If cls is None, returns the list of objects of all types currently in storage.
        If a cls is provided, returns objects of that specific type.

        Args:
            cls (class): The class type for filtering objects.

        Returns:
            dict: A dictionary of instantiated objects, optionally filtered by class type.
        """
        if cls:
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to the storage dictionary.

        Args:
            obj (BaseModel): The object to be added to storage.
        """
        key = f'{obj.__class__.__name__}.{obj.id}'
        self.__objects[key] = obj

    def save(self):
        """
        Serializes the storage dictionary to the JSON file (__file_path).
        """
        obj_dict = {obj_id: obj.to_dict() for obj_id, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects, if __file_path exists.
        Otherwise, does nothing.
        """
        try:
            with open(self.__file_path, 'r') as f:
                obj_dict = json.load(f)
            for obj_id, obj_attrs in obj_dict.items():
                self.__objects[obj_id] = eval(obj_attrs['__class__'])(**obj_attrs)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside.

        Args:
            obj (BaseModel): The object to delete from storage.
        """
        if obj:
            key = f'{obj.__class__.__name__}.{obj.id}'
            if key in self.__objects:
                del self.__objects[key]

    def classes(self):
        """
        Returns a dictionary of valid model classes and their references.
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        return {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
