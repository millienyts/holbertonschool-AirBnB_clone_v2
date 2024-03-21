#!/usr/bin/python3
#!/usr/bin/python3
"""
Review Module for HBNB project.
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    __tablename__ = 'reviews'
    text = Column(String(1024), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)

    # Ensure that back_populates or backref does not conflict with existing properties
    user = relationship("User", back_populates="reviews")
    place = relationship("Place", back_populates="reviews")
