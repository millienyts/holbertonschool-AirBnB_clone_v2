#!/usr/bin/python3
"""
State Module for the HBNB project.

This module defines the State class, which represents the geographical state
in which cities are located. It supports two types of storage: database storage
using SQLAlchemy and file storage, with dynamic functionality based on the
storage type.
"""

from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from os import getenv
import models
from models.city import City

class State(BaseModel, Base):
    """
    Represents a state in the application.

    Attributes:
        __tablename__ (str): The name of the table for SQLAlchemy.
        name (Column): The name of the state, a non-nullable string.
        cities (relationship or property): A list of City objects associated
            with the state. This can be a SQLAlchemy relationship or a
            dynamically computed property, depending on the storage type.

    The behavior of the `cities` attribute changes based on the storage backend.
    In database storage mode, it directly uses a SQLAlchemy relationship to fetch
    related City objects. In file storage mode, it computes the list of cities
    dynamically, filtering them by `state_id`.
    """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        # For database storage, establish a relationship with the City class.
        # This allows for direct fetching of City objects associated with a State.
        cities = relationship('City', backref='state', cascade='all, delete-orphan')
    else:
        # In file storage mode, the `cities` attribute is a property that
        # dynamically computes the list of City objects associated with this State.
        @property
        def cities(self):
            """
            Getter for cities in the case of file storage.

            Returns:
                list: A list of City instances that are associated with this State.
            """
            cities_in_state = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    cities_in_state.append(city)
            return cities_in_state
