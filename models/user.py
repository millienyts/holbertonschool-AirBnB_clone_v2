#!/usr/bin/python3
"""
Module that defines the User class.

This module defines the User class for the HBnB project, representing an
application user with various personal and authentication attributes.
It also outlines relationships with other models such as Place and Review,
showcasing how users are connected to other components within the application.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """
    Defines a user within the HBnB application.

    Attributes:
        __tablename__ (str): Name of the table for storing user records in the database.
        email (Column): Email address of the user, required for authentication.
        password (Column): Password for user authentication, stored securely.
        first_name (Column): User's first name, optional.
        last_name (Column): User's last name, optional.
        places (relationship): A list of Place instances associated with the user.
                               Defines a one-to-many relationship indicating places
                               created by the user.
        reviews (relationship): A list of Review instances created by the user.
                                This establishes a one-to-many relationship with reviews
                                authored by the user.

    The User class includes essential fields for authentication (email and password) and
    personal information (first and last names). It employs SQLAlchemy's ORM capabilities
    for relational mapping and supports cascading delete operations for related Place and
    Review instances, ensuring data integrity and ease of management.
    """
    
    __tablename__ = "users"

    # Authentication and personal information fields
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    # Establishing relationships with the Place and Review models
    places = relationship('Place', backref='user', cascade='all, delete-orphan')
    reviews = relationship('Review', backref='user', cascade='all, delete-orphan')
