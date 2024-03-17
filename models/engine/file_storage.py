#!/usr/bin/python3
"""
FileStorage module for the AirBnB clone project.
This module handles serialization and deserialization of Python objects to and from JSON format, providing a simple file-based persistence mechanism.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
    """
    A class that serializes instances to a JSON file and deserializes JSON files back to instances.

    Attributes:
        __file_path (str): The path to the JSON file where objects are stored.
        __objects (dict): A dictionary to store all objects by <class name>.<id>.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Retrieves the dictionary of stored objects, optionally filtered by class type.

        Args:
            cls (class): The class to filter objects by.

        Returns:
            dict: A dictionary of stored objects, optionally filtered.
        """
        if cls:
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to the storage dictionary.

        Args:
            obj (BaseModel): The object to be stored.
        """
        if obj:
            self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """
        Serializes the storage dictionary to the JSON file specified by __file_path.
        """
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects, if __file_path exists.
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                obj_dicts = json.load(f)
                for obj_id, obj_dict in obj_dicts.items():
                    self.__objects[obj_id] = eval(obj_dict["__class__"])(**obj_dict)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside.

        Args:
            obj (BaseModel): The object to delete.
        """
        obj_key = f"{obj.__class__.__name__}.{obj.id}" if obj else None
        if obj_key and obj_key in self.__objects:
            del self.__objects[obj_key]

    def close(self):
        """
        Calls reload() for deserializing the JSON file to objects.
        """
        self.reload()
