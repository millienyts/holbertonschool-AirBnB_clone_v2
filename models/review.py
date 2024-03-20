#!/usr/bin/python3
"""Review module for the HBNB project"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class Review(BaseModel, Base):
    """Review class to store review information"""
    __tablename__ = 'reviews'
    if 'HBNB_TYPE_STORAGE' in os.environ and os.environ['HBNB_TYPE_STORAGE'] == 'db':
        # These columns and relationships are only created if working with DBStorage
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        # Relationship with the Place and User models
        place = relationship("Place", back_populates="reviews")
        user = relationship("User", back_populates="reviews")
    else:
        # Attributes for FileStorage
        place_id = ""
        user_id = ""
        text = ""
