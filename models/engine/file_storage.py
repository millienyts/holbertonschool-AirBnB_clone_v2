import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """Represents a file storage for HBnB objects."""
    
    __file_path = 'file.json'  # Path to the JSON file
    __objects = {}  # Dictionary to store all objects

    def all(self, cls=None):
        """
        Returns a dictionary of all objects.
        Optionally filters by class.
        
        Args:
            cls (str or None): Class name to filter objects by.
        
        Returns:
            dict: A dictionary of filtered or all stored objects.
        """
        if cls:
            return {k: v for k, v in FileStorage.__objects.items() if isinstance(v, cls)}
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new object to the storage dictionary.
        
        Args:
            obj (BaseModel): The object to be stored.
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        obj_dict = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            json.dump(obj_dict, f)

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside.
        
        Args:
            obj (BaseModel, optional): The object to delete. Defaults to None.
        """
        if obj:
            obj_key = f"{obj.__class__.__name__}.{obj.id}"
            if obj_key in FileStorage.__objects:
                del FileStorage.__objects[obj_key]

    def reload(self):
        """
        Deserializes the JSON file to __objects, if it exists.
        """
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                obj_dict = json.load(f)
            for obj_id, obj_data in obj_dict.items():
                cls_name = obj_data['__class__']
                cls = eval(cls_name)
                self.new(cls(**obj_data))
        except FileNotFoundError:
            pass
