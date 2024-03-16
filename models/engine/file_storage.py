import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """Manages storage of hbnb models in JSON format."""
    
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        If cls is provided, returns a dictionary of objects of that class.
        """
        if cls is None:
            return FileStorage.__objects
        elif isinstance(cls, str):
            cls = eval(cls)
        return {k: v for k, v in FileStorage.__objects.items() if isinstance(v, cls)}

    def new(self, obj):
        """Adds new object to storage dictionary."""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            FileStorage.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file."""
        obj_dict = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            json.dump(obj_dict, f)

    def delete(self, obj=None):
        """
        Delete obj from __objects if inside.
        If obj is None, the method does nothing.
        """
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            FileStorage.__objects.pop(key, None)

    def reload(self):
        """Loads storage dictionary from file if it exists."""
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                obj_dict = json.load(f)
            for k, v in obj_dict.items():
                cls_name = v['__class__']
                cls = eval(cls_name)
                FileStorage.__objects[k] = cls(**v)
        except FileNotFoundError:
            pass

    def close(self):
        """Call reload method for deserializing the JSON file to objects."""
        self.reload()
