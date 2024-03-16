#!/usr/bin/python3
"""Defines the Place class."""
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# Define the many-to-many relationship table
place_amenity = Table('place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)

class Place(BaseModel, Base):
    """Represents a Place for a user."""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    # Other Place attributes...
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)

    # FileStorage relationship between Place and Amenity
    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def amenities(self):
            """Returns the list of Amenity instances."""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """Adds an Amenity.id to the amenity_ids."""
            if type(obj).__name__ == 'Amenity':
                self.amenity_ids.append(obj.id)
