#!/usr/bin/python3
"""
Place Module for HBNB project
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

# Define the association table for a many-to-many relationship between Place and Amenity
place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey(
                          'places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Relationship with User
    user = relationship("User", back_populates="places")

    # For DBStorage: Defines the many-to-many relationship between Place and Amenity
    amenities = relationship("Amenity", secondary=place_amenity,
                             back_populates="place_amenities", viewonly=False)

    # For FileStorage: Define amenity_ids as a list of Amenity.id
    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def amenities(self):
            """Returns the list of Amenity instances from amenity_ids"""
            from models import storage
            from models.amenity import Amenity
            amenity_list = []
            for amenity_id in self.amenity_ids:
                amenity = storage.all(Amenity).get(
                    'Amenity.{}'.format(amenity_id))
                if amenity:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """Adds an Amenity.id to the amenity_ids list"""
            if type(obj).__name__ == 'Amenity':
                if hasattr(self, 'amenity_ids'):
                    self.amenity_ids.append(obj.id)
                else:
                    self.amenity_ids = [obj.id]

# Ensure the relationship is set up in Amenity model too


class Amenity(BaseModel, Base):
    """ Amenity model """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship(
        "Place", secondary=place_amenity, back_populates="amenities", viewonly=False)
