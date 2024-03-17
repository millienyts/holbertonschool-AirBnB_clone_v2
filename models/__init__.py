#!/usr/bin/python3
"""
Initialize the models package.
"""

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
import os

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}

storage = None
storage_t = os.getenv('HBNB_TYPE_STORAGE')

if storage_t == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
