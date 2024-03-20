#!/usr/bin/python3
""" Amenity module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'
    # Column definitions
    name = Column(String(128), nullable=False)
    # SQLAlchemy relationship for DBStorage
    places = relationship("Place", secondary="place_amenity",
                          back_populates="amenities")
