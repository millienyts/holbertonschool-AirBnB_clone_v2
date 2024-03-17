#!/usr/bin/python3
"""Defines the FileStorage class."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances."""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage.
        If cls is provided, returns a dictionary of objects of type cls.
        """
        if cls:
            cls_dict = {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary."""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        obj_dict = {obj: self.__objects[obj].to_dict() for obj in self.__objects.keys()}
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def delete(self, obj=None):
        """Deletes obj from __objects if it’s inside."""
        if obj:
            obj_id = f"{obj.__class__.__name__}.{obj.id}"
            if obj_id in self.__objects:
                del self.__objects[obj_id]

    def reload(self):
        """Deserializes the JSON file to __objects, if it exists."""
        try:
            with open(self.__file_path, 'r') as f:
                obj_dict = json.load(f)
            for obj in obj_dict:
                self.__objects[obj] = eval(obj_dict[obj]['__class__'])(**obj_dict[obj])
        except FileNotFoundError:
            pass

