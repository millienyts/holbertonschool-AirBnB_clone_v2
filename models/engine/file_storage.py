#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        Optionally, returns objects of a specific class.
        """
        if cls:
            # Use isinstance for type checking, fix for E721
            class_name = cls.__name__ if isinstance(cls, type) else cls
            return {
                k: v for k, v in FileStorage.__objects.items()
                if k.split('.')[0] == class_name
            }
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
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review
        }

        try:
            with open(FileStorage.__file_path, "r") as f:
                objects = json.load(f)
                for obj_id, obj_dict in objects.items():
                    cls_name = obj_dict["__class__"]
                    if cls_name in classes:
                        # Breaking the following line to comply with E501
                        self.__objects[obj_id] = classes[cls_name](**obj_dict)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
