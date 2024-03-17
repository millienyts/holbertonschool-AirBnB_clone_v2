#!/usr/bin/python3
"""
Enhanced DBStorage class using SQLAlchemy for the AirBnB clone project.
This module manages database sessions and interactions, including creation,
querying, and deletion of records.
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DBStorage:
    """
    Handles interactions with the MySQL database through SQLAlchemy ORM.
    It supports creating tables, adding new objects, and querying the database.
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes DBStorage instance with database connection."""
        self.__engine = create_engine(
            f"mysql+mysqldb://{getenv('HBNB_MYSQL_USER')}:" \
            f"{getenv('HBNB_MYSQL_PWD')}@{getenv('HBNB_MYSQL_HOST')}/" \
            f"{getenv('HBNB_MYSQL_DB')}", pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries all objects of a given class from the database.
        If no class is specified, queries all objects of all types.
        """
        obj_dict = {}
        classes = [State, City, User, Place, Review, Amenity] if not cls else [cls]
        for model in classes:
            for obj in self.__session.query(model).all():
                obj_dict[f"{obj.__class__.__name__}.{obj.id}"] = obj
        return obj_dict

    def new(self, obj):
        """Adds a new object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session if not None."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Recreates all tables in the database and starts a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        ScopedSession = scoped_session(session_factory)
        self.__session = ScopedSession()

    def close(self):
        """Closes the current SQLAlchemy session."""
        self.__session.close()
