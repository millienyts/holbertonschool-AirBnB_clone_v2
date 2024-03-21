from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

# Association table for Place-Amenity many-to-many relationship, only relevant for DBStorage
if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
        'place_amenity', Base.metadata,
        Column('place_id', String(60), ForeignKey(
            'places.id'), primary_key=True),
        Column('amenity_id', String(60), ForeignKey(
            'amenities.id'), primary_key=True)
    )


class Place(BaseModel, Base):
    __tablename__ = 'places'
    # Column definitions
    # (Keep as is from your provided snippet...)

    # Relationships
    user = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place",
                           cascade="all, delete-orphan")

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship(
            "Amenity", secondary=place_amenity, back_populates="places", viewonly=False)
    else:
        @property
        def reviews(self):
            """FileStorage: Getter for reviews."""
            from models import storage
            from models.review import Review
            return [review for review in storage.all(Review).values() if review.place_id == self.id]

        @property
        def amenities(self):
            """FileStorage: Getter for amenities."""
            from models import storage
            from models.amenity import Amenity
            return [amenity for amenity in storage.all(Amenity).values() if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """FileStorage: Setter for adding an Amenity ID to the amenity list."""
            if not hasattr(self, 'amenity_ids'):
                self.amenity_ids = []
            if obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
    # Adjust the relationship for 'reviews' to ensure it works with FileStorage
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship(
            "Review", back_populates="place", cascade="all, delete-orphan")
    else:
        @property
        def reviews(self):
            """FileStorage: Getter for reviews"""
            from models import storage
            from models.review import Review
            return [review for review in storage.all(Review).values() if review.place_id == self.id]
