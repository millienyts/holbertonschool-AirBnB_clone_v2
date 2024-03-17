#!/usr/bin/python3
"""
Enhanced Database Storage module using SQLAlchemy.
This module defines a class that manages database interactions.
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

class EnhancedDBStorage:
    """
    Handles storage actions with a SQL database using SQLAlchemy ORM.
    
    Attributes:
        engine: SQLAlchemy engine connected to the database.
        session: Scoped session for executing ORM queries.
    """

    engine = None
    session = None

    def __init__(self):
        """Initializes the EnhancedDBStorage instance."""
        USER = getenv("HBNB_MYSQL_USER")
        PASSWORD = getenv("HBNB_MYSQL_PWD")
        DATABASE = getenv("HBNB_MYSQL_DB")
        HOST = getenv("HBNB_MYSQL_HOST")
        ENVIRONMENT = getenv("HBNB_ENV")

        self.engine = create_engine(f'mysql+mysqldb://{USER}:{PASSWORD}@{HOST}/{DATABASE}',
                                    pool_pre_ping=True)

        if ENVIRONMENT == "test":
            Base.metadata.drop_all(self.engine)

    def aggregate(self, cls=None):
        """
        Fetches all objects of a given class from the database.
        
        If no class is provided, fetches all objects of all classes.

        Args:
            cls: The class to fetch objects for.

        Returns:
            A dictionary of fetched objects.
        """
        object_dict = {}
        if cls:
            objects = self.session.query(cls).all()
            for obj in objects:
                key = f"{obj.__class__.__name__}.{obj.id}"
                object_dict[key] = obj
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for model_class in classes:
                objects = self.session.query(model_class).all()
                for obj in objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    object_dict[key] = obj
        return object_dict

    def insert(self, obj):
        """
        Adds a new object to the current database session.
        
        Args:
            obj: The object to add.
        """
        self.session.add(obj)

    def persist(self):
        """Commits all changes to the current session to the database."""
        self.session.commit()

    def expunge(self, obj=None):
        """
        Deletes an object from the current database session.

        Args:
            obj: The object to delete. If None, no action is taken.
        """
        if obj:
            self.session.delete(obj)

    def reinitialize(self):
        """
        Reloads the database schema and initializes a new session.
        """
        Base.metadata.create_all(self.engine)
        session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        ScopedSession = scoped_session(session_factory)
        self.session = ScopedSession()

    def terminate(self):
        """
        Closes the current session.
        """
        self.session.close()
