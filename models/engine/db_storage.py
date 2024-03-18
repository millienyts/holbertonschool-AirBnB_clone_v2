#!/usr/bin/python3
"""
Database storage engine for the HBnB project.

This module provides the DBStorage class, which manages database sessions
and operations for the HBnB application, utilizing SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class DBStorage:
    """
    Handles long-term storage of all class instances to a database.

    Attributes:
        __engine (Engine): SQLAlchemy engine instance.
        __session (Session): SQLAlchemy session.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the DBStorage instance, creating the engine and dropping
        all tables if the environment is set to 'test'.
        """
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        db_url = f"mysql+mysqldb://{user}:{pwd}@{host}:3306/{db}"
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        Queries the current database session for all objects of a certain
        class. If no class is specified, queries for all known classes.

        Args:
            cls (str): The class name to query for.

        Returns:
            dict: A dictionary of queried objects, with key format '<class name>.<object id>'.
        """
        obj_dict = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f'{cls.__name__}.{obj.id}'
                obj_dict[key] = obj
        else:
            for class_name in self.classes():
                class_ = self.classes()[class_name]
                objs = self.__session.query(class_).all()
                for obj in objs:
                    key = f'{class_.__name__}.{obj.id}'
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Adds a new object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the current database session, if not None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads all tables from the database and recreates the session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        ScopedSession = scoped_session(session_factory)
        self.__session = ScopedSession()

    def classes(self):
        """
        Returns a dictionary of valid model classes and their references.
        """
        class_dict = {
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
        return class_dict
