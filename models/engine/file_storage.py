#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage
        If cls is provided, returns a dictionary of objects of type cls.
        """
        if cls:
            cls_objects = {k: v for k,
                           v in self.__objects.items() if isinstance(v, cls)}
            return cls_objects
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        obj_dict = {obj_id: obj.to_dict()
                    for obj_id, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r') as f:
                obj_dict = json.load(f)
            for obj_id, obj_data in obj_dict.items():
                cls_name = obj_data['__class__']
                cls = globals()[cls_name]
                self.__objects[obj_id] = cls(**obj_data)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def close(self):
        """Call reload() method for deserializing the JSON file to objects."""
        self.reload()

# Assuming cmd is your command line interface object
# and FileStorage is correctly set up and integrated


def execute_command(command, storage):
    if command.startswith("create"):
        parts = command.split()
        model_name = parts[1]
        attributes = " ".join(parts[2:])
        model_class = globals().get(model_name)

        if model_class:
            instance = model_class()
            for attr in attributes.split(","):
                key, val = attr.split("=")
                setattr(instance, key, val.strip('"'))
            storage.new(instance)
            storage.save()
            print(f"New ID: {instance.id}")
        else:
            print(f"Model {model_name} not found")


storage = FileStorage()
storage.reload()

# Example usage
commands = [
    'create State name="California"',
    # Add other commands as per your tests
]

for command in commands:
    execute_command(command, storage)
