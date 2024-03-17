#!/usr/bin/python3
"""Module for FileStorage class."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
    """A class that serializes instances to a JSON file and
    deserializes JSON file to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage.
        
        Args:
            cls (None, optional): The class to filter objects by.

        Returns:
            dict: A dictionary of stored objects, filtered by class if provided.
        """
        if cls is None:
            return self.__objects
        else:
            cls_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    cls_dict[key] = value
            return cls_dict

    def new(self, obj):
        """Adds new object to storage dictionary.

        Args:
            obj (BaseModel): The object to add.
        """
        self.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        obj_dict = {obj: self.__objects[obj].to_dict() for obj in self.__objects.keys()}
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(self.__file_path, 'r') as f:
                objs = json.load(f)
            for obj in objs.values():
                cls_name = obj['__class__']
                del obj['__class__']
                self.new(eval(cls_name)(**obj))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it’s inside - if obj is equal to None, the method should not do anything.
        
        Args:
            obj (BaseModel, optional): The object to delete.
        """
        if obj is None:
            return

        # Construct the key in the format ClassName.id
        key = "{}.{}".format(type(obj).__name__, obj.id)
        
        # Check and delete the object if it exists in the __objects dictionary
        if key in self.__objects:
            del self.__objects[key]


    def close(self):
        """Call reload() method for deserializing the JSON file to objects."""
        self.reload()
