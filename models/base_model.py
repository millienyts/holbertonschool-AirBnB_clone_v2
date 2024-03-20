#!/usr/bin/python3
"""
Place Module for HBNB project
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

# Association table for Place-Amenity many-to-many relationship
place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey(
        'places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey(
        'amenities.id'), primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """A place to stay."""
    __tablename__ = 'places'
    # Columns definition
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    # Other columns...

    # SQLAlchemy relationships
    user = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place",
                           cascade="all, delete-orphan")

    # Many-to-many relationship for DBStorage
    amenities = relationship(
        "Amenity", secondary=place_amenity, back_populates="places", viewonly=False)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        # FileStorage relationship handling
        @property
        def amenities(self):
            """FileStorage: Returns list of Amenity instances."""
            from models import storage
            from models.amenity import Amenity
            amenity_list = storage.all(Amenity).values()
            return [amenity for amenity in amenity_list if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """FileStorage: Appends Amenity.id to the list."""
            if type(obj).__name__ == 'Amenity':
                if not hasattr(self, 'amenity_ids'):
                    self.amenity_ids = []
                self.amenity_ids.append(obj.id)
