#!/usr/bin/python3
"""
This module instantiates an object of class FileStorage or DBStorage
depending on the environment variable HBNB_TYPE_STORAGE.
"""

import os

storage = None


def get_storage():
    """Function to initialize and return the storage instance."""
    global storage
    if storage is not None:
        return storage

    from models.engine.file_storage import FileStorage
    from models.engine.db_storage import DBStorage

    HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')
    if HBNB_TYPE_STORAGE == 'db':
        storage = DBStorage()
    else:
        storage = FileStorage()
    storage.reload()
    return storage


# Call get_storage() to initialize storage for  comp
storage = get_storage()
