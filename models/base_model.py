#!/usr/bin/python3
"""
This module defines the BaseModel class, serving as the foundation
for all other classes in the AirBnB clone project. It incorporates
common attributes and methods to be inherited.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import uuid
from datetime import datetime
import models

Base = declarative_base()

class BaseModel:
    """
    Defines the base structure and operations of data models, including
    id creation, timestamping, and serialization to dictionaries.
    """

    # Database table column definitions
    id = Column(String(60), primary_key=True, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """
        Initializes a new BaseModel instance, setting attributes from
        kwargs or generating default values for id, created_at, and updated_at.
        """
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = datetime.strptime(kwargs.get('created_at'), "%Y-%m-%dT%H:%M:%S.%f") if 'created_at' in kwargs else datetime.utcnow()
        self.updated_at = datetime.strptime(kwargs.get('updated_at'), "%Y-%m-%dT%H:%M:%S.%f") if 'updated_at' in kwargs else datetime.utcnow()
        for key, value in kwargs.items():
            if key not in ('id', 'created_at', 'updated_at', '__class__'):
                setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        """
        return f"[{type(self).__name__}] ({self.id}) {self.to_dict(show_id=False)}"

    def save(self):
        """
        Updates 'updated_at' with the current datetime, then saves
        the instance to the storage.
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, show_id=True):
        """
        Generates a dictionary representation of the instance, including
        all attributes and additional class and datetime information.
        
        Args:
            show_id (bool): Whether to include the 'id' field in the dictionary.
        """
        dictionary = {**self.__dict__, "__class__": type(self).__name__,
                      "created_at": self.created_at.isoformat(),
                      "updated_at": self.updated_at.isoformat()}
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        if not show_id:
            del dictionary['id']
        return dictionary

    def delete(self):
        """
        Removes the instance from the storage.
        """
        models.storage.delete(self)
