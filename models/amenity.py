#!/usr/bin/python3
"""
Defines the Amenity class.
This class represents an amenity in the application, with support for both
file storage and database storage configurations.
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

class Amenity(BaseModel, Base):
    """
    Represents an amenity with its attributes.

    Attributes:
        __tablename__ (str): The name of the table for SQLAlchemy.
        name (SQLAlchemy Column): The name of the amenity.
        place_amenities (SQLAlchemy relationship): A relationship between places
            and amenities, defined only when using a database storage (db).
    """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)

    # Establish a relationship with the Place class only if using database storage.
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = relationship(
            'Place',
            secondary='place_amenity',  # Specifies the association table.
            back_populates='amenities'  # Links back to the amenities attribute of the Place class.
        )
