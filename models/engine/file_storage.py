#!/usr/bin/python3
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

class FileStorage:
    """This class manages storage of hbnb models in JSON format.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of instantiated objects in __objects.

        If a cls is specified, returns a dictionary of objects of that type.
        Otherwise, returns the __objects dictionary.
        """
        if cls is None:
            return FileStorage.__objects
        else:
            if type(cls) == str:
                # Convert string to class if needed
                cls = eval(cls)
            return {k: v for k, v in FileStorage.__objects.items() if isinstance(v, cls)}

    def new(self, obj):
        """Add new object to storage dictionary."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            json.dump({k: v.to_dict() for k, v in FileStorage.__objects.items()}, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        classes = {'BaseModel': BaseModel, 'User': User, 'Place': Place, 'State': State, 'City': City, 'Amenity': Amenity, 'Review': Review}
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                objs = json.load(f)
                for o in objs.values():
                    cls_name = o['__class__']
                    if cls_name in classes:
                        self.new(classes[cls_name](**o))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it's inside."""
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            FileStorage.__objects.pop(key, None)

    def close(self):
        """Call the reload method for deserialization from JSON to objects."""
        self.reload()
