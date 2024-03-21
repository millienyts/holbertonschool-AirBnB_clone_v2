#!/usr/bin/python3
"""
This module instantiates an object of class FileStorage or DBStorage
depending on the environment variable HBNB_TYPE_STORAGE.
"""

from models.review import Review
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.base_model import BaseModel  # Import BaseModel if needed
import os
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Determine storage type based on environment variable
HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE', 'file')

if HBNB_TYPE_STORAGE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Ensure models are imported after storage initialization

# # Import relationships
# # Note: If 'place_amenity' is directly in one of the models, adjust accordingly
# try:
#     from models.relationships import place_amenity
# except ImportError:
#     # Handle the case where 'models/relationships.py' does not exist
#     # This can be an empty block if no action is needed
#     pass

# Reload storage to load any existing data
storage.reload()
