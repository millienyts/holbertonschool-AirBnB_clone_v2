#!/usr/bin/python3
"""
This module defines a base class for all models in our hbnb clone
"""
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class BaseModel:
    """
    A base class for all hbnb models with SQLAlchemy and FileStorage compatibility
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Instantiates a new model with potential SQLAlchemy and FileStorage compatibility
        """
        # Assign ID and timestamps if not provided in kwargs
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

        # Apply the rest of the kwargs to instance attributes
        for key, value in kwargs.items():
            if key != "__class__":
                setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the instance
        """
        cls_name = self.__class__.__name__
        return '[{}] ({}) {}'.format(cls_name, self.id, self.to_dict())

    def save(self):
        """
        Updates updated_at with current time when instance is changed
        """
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def delete(self):
        """
        Deletes the current instance from the storage
        """
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """
        Convert instance into dict format, including attributes for SQLAlchemy
        """
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = dictionary['created_at'].isoformat()
        dictionary['updated_at'] = dictionary['updated_at'].isoformat()

        # Remove SQLAlchemy instance state, if present
        dictionary.pop('_sa_instance_state', None)

        return dictionary

    @classmethod
    def close(cls):
        """
        Call remove() method on the private session attribute (self.__session)
        or close() on the class session if it's a session of the Session type
        """
        from models import storage
        storage.close()
