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
        obj_id = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[obj_id] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {obj_id: obj.to_dict() for obj_id, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(self.__file_path, 'r') as f:
                objects = json.load(f)
                for obj_id, obj_dict in objects.items():
                    class_name = obj_dict['__class__']
                    if class_name in classes:
                        self.__objects[obj_id] = classes[class_name](**obj_dict)
        except FileNotFoundError:
            pass
