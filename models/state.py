#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from os import getenv
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        # For DBStorage: Establish a relationship to cities with cascade options
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    else:
        # For FileStorage: Implement a getter property to fetch city instances
        @property
        def cities(self):
            """Getter attribute cities for FileStorage"""
            all_cities = models.storage.all(models.City)
            # Filter cities by state_id
            state_cities = [city for city in all_cities.values()
                            if city.state_id == self.id]
            return state_cities
