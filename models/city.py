#!/usr/bin/python3
"""
Defines the City class for the HBNB project.

This module provides the 'City' class which is a part of the application's data model.
Cities are stored in a database table 'cities' and each city is associated with a state.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """
    Represents a city in the database.

    Attributes:
        __tablename__ (str): The name of the table for SQLAlchemy, 'cities'.
        name (Column): The name of the city. Stored as a String with a maximum
                       of 128 characters. It is a required field, so nullable is False.
        state_id (Column): The state ID to which the city belongs. It is a ForeignKey
                           that references 'states.id', indicating the relationship
                           between cities and states. This is also a required field.
        places (relationship): A relationship that defines how 'City' objects are related
                               to 'Place' objects. Each city can have multiple places.
                               The 'backref' creates a reverse link from 'Place' to 'City',
                               named 'cities'.
    """
    # SQLAlchemy table name
    __tablename__ = 'cities'
    
    # Column definitions
    name = Column(String(128), nullable=False)  # City name
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)  # Reference to the state
    
    # Establishing the relationship with the 'Place' class. This allows each city to be associated
    # with multiple places. The 'cascade' option ensures that if a city is deleted, all of its
    # associated places are also deleted from the database to maintain referential integrity.
    places = relationship('Place', backref='cities', cascade='all, delete, delete-orphan')
