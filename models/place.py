from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

# Association table for Place-Amenity relationship
if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey(
                              'places.id'), primary_key=True, nullable=False),
                          Column('amenity_id', String(60), ForeignKey(
                              'amenities.id'), primary_key=True, nullable=False)
                          )


class Place(BaseModel, Base):
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    user = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place",
                           cascade="all, delete-orphan")

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship("Amenity",
                                 secondary=place_amenity,
                                 back_populates="places",
                                 viewonly=False)
    else:
        amenity_ids = []

        @property
        def amenities(self):
            """FileStorage: Getter for amenities."""
            if getenv('HBNB_TYPE_STORAGE') != 'db':
                from models import storage
                from models.amenity import Amenity
                return [amenity for amenity in storage.all(Amenity).values()
                        if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """FileStorage: Setter for adding an Amenity ID."""
            if getenv('HBNB_TYPE_STORAGE') != 'db':
                if not hasattr(self, 'amenity_ids'):
                    self.amenity_ids = []
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
