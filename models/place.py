#!/usr/bin/python3
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv
import models

# Association table for the many-to-many relationship between Place and Amenity
association_place_amenity = Table(
    "place_amenity", Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"), primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"), primary_key=True, nullable=False)
)

class Place(BaseModel, Base):
    """Representation of a Place within the Airbnb clone project.

    Attributes:
        city_id (str): ID of the City where the place is located.
        user_id (str): ID of the User who owns the place.
        name (str): Name of the place.
        description (str, optional): Description of the place.
        number_rooms (int): Number of rooms in the place.
        number_bathrooms (int): Number of bathrooms in the place.
        max_guest (int): Maximum number of guests the place can accommodate.
        price_by_night (int): Rental price per night.
        latitude (float, optional): Geographical latitude of the place.
        longitude (float, optional): Geographical longitude of the place.
        amenity_ids (list): If file storage is used, a list of Amenity IDs associated with the place.
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        # Reviews relationship only valid for DB storage
        reviews = relationship("Review", cascade="all, delete, delete-orphan", backref="place")
        # Many-to-many relationship with Amenities valid only for DB storage
        amenities = relationship("Amenity", secondary=association_place_amenity, back_populates="place_amenities", viewonly=False)
    else:
        @property
        def reviews(self):
            """File storage mode: Return list of Review instances with matching place_id."""
            all_reviews = models.storage.all(models.Review)
            return [review for review in all_reviews.values() if review.place_id == self.id]

        @property
        def amenities(self):
            """File storage mode: Getter for amenities based on amenity_ids list."""
            return [models.storage.all(models.Amenity)[amenity_id] for amenity_id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """File storage mode: Adds an Amenity.id to the amenity_ids list."""
            if isinstance(obj, models.Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
