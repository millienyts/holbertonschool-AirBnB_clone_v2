#!/usr/bin/python3
""" Amenity module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'
    # Define your columns
    id = Column(String(60), primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    __table_args__ = {'extend_existing': True}
