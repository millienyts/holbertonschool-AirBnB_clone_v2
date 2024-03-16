#!/usr/bin/python3
"""Module to initialize a singleton storage instance.

Depending on the environment configuration, this will select between file-based storage and database storage for managing application data persistence.
"""

from os import getenv
# Importing all necessary models for completeness and potential initialization needs.
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
# Import storage engine options.
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

# Determine storage type from environment variable and instantiate accordingly.
storage_type = getenv("HBNB_TYPE_STORAGE")
if storage_type == "db":
    storage = DBStorage()
else:
    storage = FileStorage()

# Perform initial loading/reloading of storage to ensure data is ready for use.
storage.reload()
