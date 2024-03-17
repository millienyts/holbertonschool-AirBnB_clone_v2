#!/usr/bin/python3
"""Defines the Amenity class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table
from sqlalchemy.orm import relationship

class Amenity(BaseModel, Base):
    """Represents an Amenity for a place."""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
