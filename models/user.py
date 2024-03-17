#!/usr/bin/python3
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.place import Place
from models.review import Review

class User(BaseModel, Base):
    """
    Defines the blueprint for a User entity within the system, including personal details and relational links to other entities such as Place and Review.

    Attributes:
        email (Column): The user's email address, used for logging in.
        password (Column): The user's password for authentication. In a production system, this would be hashed for security.
        first_name (Column, optional): The user's first name.
        last_name (Column, optional): The user's last name.
        places (relationship): Links to the Place instances associated with this user.
        reviews (relationship): Links to the Review instances authored by this user.
    """
    __tablename__ = "users"
    # User identification and authentication details
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    # Optional personal information for user profiles
    first_name = Column(String(128))
    last_name = Column(String(128))
    # Relational links to places listed and reviews made by the user
    places = relationship("Place", cascade="all, delete, delete-orphan", backref="user")
    reviews = relationship("Review", cascade="all, delete, delete-orphan", backref="user")
