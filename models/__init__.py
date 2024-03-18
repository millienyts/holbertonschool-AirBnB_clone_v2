#!/usr/bin/python3
"""
Module to instantiate a storage object.

This module will select the appropriate storage type for the HBNB project
based on the environment configuration. It supports both file-based storage
and database storage, selecting the latter if the HBNB_TYPE_STORAGE
environment variable is set to 'db'.
"""

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import getenv

# Determine the storage type based on the HBNB_TYPE_STORAGE environment variable.
# If 'db' is specified, use the database storage system. Otherwise, default to file storage.
if getenv("HBNB_TYPE_STORAGE") == "db":
    # Instantiate a DBStorage object for database interaction.
    storage = DBStorage()
else:
    # Instantiate a FileStorage object for file-based storage.
    storage = FileStorage()

# Regardless of the storage type chosen, call reload to ensure that any
# persisted data is loaded into the current session.
storage.reload()
