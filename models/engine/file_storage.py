#!/usr/bin/python3
"""Module for handling persistent storage of application objects."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class PersistentStorage:
    """Handles JSON serialization and deserialization of app entities."""
    storage_file = 'file.json'
    object_registry = {}

    def all(self, cls=None):
        """Fetches all objects, optionally filtered by class type."""
        if cls:
            filtered_objects = {}
            for key, obj in self.object_registry.items():
                if isinstance(obj, cls) or cls.__name__ == obj.__class__.__name__:
                    filtered_objects[key] = obj
            return filtered_objects
        return self.object_registry

    def new(self, obj):
        """Registers a new object."""
        obj_id = f"{obj.__class__.__name__}.{obj.id}"
        self.object_registry[obj_id] = obj

    def save(self):
        """Writes the registered objects to the disk."""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json_objects = {k: v.to_dict() for k, v in self.object_registry.items()}
            json.dump(json_objects, f)

    def reload(self):
        """Populates the registry with objects stored on the disk."""
        model_classes = {
            'BaseModel': BaseModel, 'User': User, 'State': State,
            'City': City, 'Amenity': Amenity, 'Place': Place, 'Review': Review
        }
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                objects = json.load(f)
                for obj_id, obj_attrs in objects.items():
                    self.object_registry[obj_id] = model_classes[obj_attrs['__class__']](**obj_attrs)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Removes an object from the registry."""
        if obj:
            obj_key = f"{obj.__class__.__name__}.{obj.id}"
            self.object_registry.pop(obj_key, None)

    def close(self):
        """Alias for the reload() method for compatibility."""
        self.reload()
