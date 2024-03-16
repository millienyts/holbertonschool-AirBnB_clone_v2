import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """Class for serializing instances to a JSON file and deserializing back."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        If cls is provided, returns only items of that class type.
        """
        if cls is not None:
            filtered_dict = {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
            return filtered_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary."""
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

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
                class_name = obj['__class__']
                del obj['__class__']
                self.new(eval(class_name)(**obj))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside.
        If obj is equal to None, the method should not do anything.
        """
        if obj is not None:
            obj_key = "{}.{}".format(type(obj).__name__, obj.id)
            if obj_key in self.__objects:
                del self.__objects[obj_key]
                self.save()
