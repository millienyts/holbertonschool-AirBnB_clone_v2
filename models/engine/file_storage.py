#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


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
                cls = globals().get(cls_name, None)
                if cls:
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


def execute_command(command, storage):
    if command.startswith("create"):
        parts = command.split()
        model_name = parts[0] if len(parts) > 1 else None
        attributes = parts[1:]

        if model_name and model_name in globals():
            model_class = globals()[model_name]
            instance = model_class()
            for attr in attributes:
                key, val = attr.split("=")
                # Convert attribute value from string to correct type
                if '"' in val:
                    val = val.strip('"').replace('_', ' ')
                elif '.' in val:
                    val = float(val)
                else:
                    val = int(val)
                setattr(instance, key, val)
            instance.save()
            print(f"New ID: {instance.id}")
        else:
            print(
                "** class doesn't exist **" if model_name else "** class name missing **")


storage = FileStorage()
storage.reload()
