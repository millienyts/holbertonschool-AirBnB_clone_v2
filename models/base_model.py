#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models import storage

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
        else:
            kwargs['updated_at'] = datetime.strptime(
                kwargs.get('updated_at'), '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(
                kwargs.get('created_at'), '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{}] ({}) {}'.format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def delete(self):
        """Delete the current instance from the storage"""
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = type(self).__name__
        dictionary['created_at'] = dictionary['created_at'].isoformat()
        dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        dictionary.pop('_sa_instance_state', None)
        return dictionary
