#!/usr/bin/python3
"""
Review Module for the HBNB project.

This module provides the Review class, a part of the application's data model that handles
reviews left by users for various places. It supports integration with a SQL database
via SQLAlchemy for persistent storage.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class Review(BaseModel, Base):
    """
    Represents a review left by a user for a place.

    Attributes:
        __tablename__ (str): Name of the table for SQLAlchemy, 'reviews'.
        place_id (Column): The ID of the place being reviewed, linked to 'places.id'.
                           It is a required field, so 'nullable' is set to False.
        user_id (Column): The ID of the user who wrote the review, linked to 'users.id'.
                          This is also a required field, ensuring every review can be traced
                          back to its author.
        text (Column): The content of the review. Stored as a String with a maximum length
                       of 1024 characters. This field is required.
    """
    __tablename__ = "reviews"

    # Defines the columns for the 'reviews' table
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)  # Establishes a ForeignKey link to the 'places' table.
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)    # Establishes a ForeignKey link to the 'users' table.
    text = Column(String(1024), nullable=False)                             # Stores the review text.
