#!/usr/bin/python3
"""Define FileStorage to serialize and deserialize JSON files."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
    """Represents a file storage system."""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Return the dictionary of objects, optionally filtered by class.
        """
        if cls:
            filtered_dict = {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
            return filtered_dict
        return self.__objects

    def new(self, obj):
        """
        Sets the obj in __objects with key <obj class name>.id
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (__file_path).
        """
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects, if it exists.
        """
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                obj_dict = json.load(f)
                for obj in obj_dict.values():
                    cls_name = obj['__class__']
                    self.new(eval(cls_name)(**obj))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside.
        """
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def close(self):
        """
        Call reload() method for deserializing the JSON file to objects.
        """
        self.reload()
