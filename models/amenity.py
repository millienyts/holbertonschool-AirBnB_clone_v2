# models/amenity.py
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    # Use the string name for `secondary` to avoid direct imports and help with the resolution at query time.
    places = relationship("Place", secondary="place_amenity",
                          back_populates="amenities")

    # DBStorage: Establish relationship only if using DBStorage
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        # Make sure 'place_amenity' is defined in 'models.place' and is imported here correctly
        # Assuming 'place_amenity' is correctly imported from 'place.py'
        from models.place import place_amenity
