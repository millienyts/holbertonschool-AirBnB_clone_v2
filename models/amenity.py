#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity_association

class EnhancedAmenity(BaseModel, Base):
    """

    Attributes:
        __tablename__ (str): The name of the MySQL table to store amenities.
        name (SQLAlchemy Column): Stores the name of the amenity, cannot be null.
        linked_places (SQLAlchemy relationship): Establishes a many-to-many
            relationship between places and amenities through an association table.
    """
    __tablename__ = "enhanced_amenities"
    name = Column(String(128), nullable=False)
    linked_places = relationship(
        "Place",
        secondary=place_amenity_association,
        back_populates="amenities"
    )
