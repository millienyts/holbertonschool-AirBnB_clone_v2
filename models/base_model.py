#!/usr/bin/python3
""" Base Model Module """
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import uuid

Base = declarative_base()


class BaseModel:
    """ Defines all common attributes/methods for other classes """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """ Initializes the BaseModel """

        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.utcnow()

        if kwargs:
            for k, v in kwargs.items():
                if k != "__class__":
                    setattr(self, k, v)

    def save(self):
        """ Updates the updated_at attribute and saves it to the storage """

        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """ Deletes the current instance from storage """

        models.storage.delete(self)

    def to_dict(self):
        """ Returns a dictionary containing all keys/values of __dict__ """

        new_dict = dict(self.__dict__)
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()

        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        return new_dict
