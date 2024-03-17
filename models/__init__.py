#!/usr/bin/python3
"""
Initialize the models package.
"""

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
import os

storage = None
storage_t = os.getenv('HBNB_TYPE_STORAGE')

if storage_t == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
