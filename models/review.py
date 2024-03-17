#!/usr/bin/python3
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base

class Review(BaseModel, Base):
    """
    Represents a review for a Place in the AirBnB clone project.

    A Review object links to a Place and a User, indicating the reviewer and the accommodation reviewed.

    Attributes:
        text (Column): Description or content of the review.
        place_id (Column): ID of the Place the review is associated with.
        user_id (Column): ID of the User who wrote the review.
    """
    __tablename__ = 'reviews'
    # Detailed review text with a substantial character limit to allow for thorough feedback.
    text = Column(String(1024), nullable=False)
    # Identifiers for the place and user to maintain relationships within the database.
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
