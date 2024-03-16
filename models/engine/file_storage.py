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
        """Returns a dictionary of models currently in storage."""
        if cls is None:
            return FileStorage.__objects
        elif isinstance(cls, str):
            # Convert cls string to actual class if necessary
            cls = eval(cls) if cls in FileStorage.__objects else None
        return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}

    def new(self, obj):
        """Adds new object to storage dictionary."""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            FileStorage.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file."""
        obj_dict = {obj: self.__objects[obj].to_dict() for obj in self.__objects}
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            json.dump(obj_dict, f)

    def delete(self, obj=None):
        """Delete obj from __objects if inside."""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def reload(self):
        """Loads storage dictionary from file if it exists."""
        classes = {'BaseModel': BaseModel, 'User': User, 'Place': Place, 'State': State, 'City': City, 'Amenity': Amenity, 'Review': Review}
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                obj_dict = json.load(f)
                for obj in obj_dict.values():
                    cls_name = obj['__class__']
                    if cls_name in classes:
                        self.new(classes[cls_name](**obj))
        except FileNotFoundError:
            pass

    def close(self):
        """Call the reload method for deserialization from JSON file to objects."""
        self.reload()
