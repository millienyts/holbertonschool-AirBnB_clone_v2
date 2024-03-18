#!/usr/bin/python3
"""
Defines the base class for all models in the hbnb clone project.

This module contains the BaseModel class, which serves as a foundation for all other model classes
in the application. It includes common attributes and methods that are shared across models.
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models

# Generates a base class for declarative class definitions.
Base = declarative_base()

class BaseModel:
    """
    A base class that defines common attributes and methods for other models.

    Attributes:
        id (Column): A unique string identifier for each instance, automatically generated.
        created_at (Column): A datetime indicating when an instance was created, automatically set.
        updated_at (Column): A datetime indicating when an instance was last updated, automatically set.
    """

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new model instance. If the instance is created with properties,
        it sets them according to the kwargs dictionary. Automatically generates a unique id
        and sets the created_at and updated_at attributes to the current datetime if not provided.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            self.id = kwargs.get("id", str(uuid.uuid4()))
            now = datetime.now()
            self.created_at = kwargs.get("created_at", now)
            self.updated_at = kwargs.get("updated_at", now)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """
        Returns a string representation of the instance, including the class name,
        id, and dictionary of attributes.
        """
        cls_name = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls_name, self.id, self.__dict__)

    def save(self):
        """
        Updates the updated_at attribute to the current datetime and saves the instance to the storage.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Converts the instance into a dictionary format, including the class name for serialization
        purposes and formats datetime attributes to ISO format.
        """
        my_dict = {key: value for key, value in self.__dict__.items() if key != '_sa_instance_state'}
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict

    def delete(self):
        """
        Deletes the current instance from the storage by calling the delete method.
        """
        models.storage.delete(self)
