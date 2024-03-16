#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
import models

class City(BaseModel, Base):
    """The city class, contains state ID and name."""
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    
    if models.storage_t == 'db':
        # For DBStorage: Define relationships to State and Place
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', backref='city', cascade='all, delete')
    else:
        # For FileStorage: Simply define state_id, no direct SQL relationship
        state_id = ''

    def __init__(self, *args, **kwargs):
        """
        Initializes a new City instance.
        For FileStorage, `state_id` needs to be managed manually.
        """
        super().__init__(*args, **kwargs)
        if models.storage_t != 'db':
            if 'state_id' in kwargs:
                self.state_id = kwargs['state_id']
