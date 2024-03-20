#!/usr/bin/python3
"""
This module instantiates an object of class FileStorage or DBStorage
depending on the environment variable HBNB_TYPE_STORAGE.
"""

import os
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

# Determine the storage type to use based on the HBNB_TYPE_STORAGE environment variable
storage_type = os.getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    # If the environment variable is 'db', use the DBStorage class
    storage = DBStorage()
else:
    # Otherwise (including when the environment variable is not set), use FileStorage
    storage = FileStorage()

# Regardless of the storage type, call reload to initialize the storage system
storage.reload()
