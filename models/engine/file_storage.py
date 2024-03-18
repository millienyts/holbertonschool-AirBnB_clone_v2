#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns a dictionary of models currently in storage"""
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = '{}.{}'.format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(temp, f)

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj is not None:
        key = "{}.{}".format(type(obj).__name__, obj.id)
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]

       def reload(self):
        """Reloads the JSON file to __objects"""
        from models.base_model import BaseModel
        # Import other classes as needed
        
        classes = {
            "BaseModel": BaseModel,
            # Add other classes here
        }
    try:
            with open(FileStorage.__file_path, "r") as f:
             objects = json.load(f)
             for obj_id, obj_dict in objects.items():
                cls_name = obj_dict["__class__"]
                if cls_name in classes:
                   self.__objects[obj_id] = classes[cls_name](**obj_dict)
    except (FileNotFoundError, json.JSONDecodeError):
    pass