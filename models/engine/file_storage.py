#!/usr/bin/python3
"""Defines the FileStorage class for AirBnB clone project."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex

class EnhancedFileStorage:
    """Handles serialization and deserialization of AirBnB clone instances.

    This class manages the storage of the application's data to a JSON file
    and the retrieval of this data from the file to application instances.

    Attributes:
        filePath: Path to the JSON data file.
        objects: A dictionary holding all objects by <class name>.<id>.
    """

    filePath = "file.json"
    objects = {}

    def retrieve_all(self, cls=None):
        """Retrieve all objects of a certain class.
        
        If no class is provided, returns all objects.
        
        Args:
            cls: The class of objects to retrieve.

        Returns:
            A dictionary of objects filtered by class if specified, else all objects.
        """
        if cls:
            filtered_objects = {}
            for obj_id, obj_instance in self.objects.items():
                if obj_id.startswith(cls.__name__):
                    filtered_objects[obj_id] = obj_instance
            return filtered_objects
        else:
            return self.objects

    def add(self, obj):
        """Add a new object to storage.

        The object is added to the `objects` dictionary with a key in the format
        <class name>.<id>.

        Args:
            obj: The object to add to storage.
        """
        if obj:
            self.objects[f"{type(obj).__name__}.{obj.id}"] = obj

    def commit(self):
        """Commit all changes to the JSON file."""
        with open(self.filePath, 'w', encoding="UTF-8") as f:
            json.dump({k: v.to_dict() for k, v in self.objects.items()}, f)

    def refresh(self):
        """Reload data from the JSON file to the application."""
        try:
            with open(self.filePath, 'r', encoding="UTF-8") as f:
                self.objects = {k: eval(v["__class__"])(**v) for k, v in json.load(f).items()}
        except FileNotFoundError:
            pass

    def discard(self, obj=None):
        """Remove an object from storage.

        Args:
            obj: The object to remove. If `None`, no action is taken.
        """
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            if key in self.objects:
                del self.objects[key]

    def conclude(self):
        """Alias for the reload method, refreshing stored data."""
        self.refresh()
