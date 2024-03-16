#!/usr/bin/python3
"""
BaseModel for HBNB project.
"""

import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from datetime import datetime

Base = declarative_base()


class BaseModel:
    """
    The BaseModel class from which future classes will be derived.
    """

    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initialization of the base model.
        """
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
            if 'created_at' in kwargs:
                self.created_at = datetime.strptime(kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if 'updated_at' in kwargs:
                self.updated_at = datetime.strptime(kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')

    def __str__(self):
        """
        String representation of the BaseModel class.
        """
        return '[{}] ({}) {}'.format(self.__class__.__name__, self.id, self.to_dict())

    def save(self):
        """
        Updates the attribute 'updated_at' with the current datetime.
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__ of the instance.
        """
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in my_dict:
            del my_dict['_sa_instance_state']
        return my_dict

    def delete(self):
        """
        Deletes the current instance from the storage (models.storage).
        """
        models.storage.delete(self)
