from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv

class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    
    # Define the association table between Amenity and Place
    place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True),
        Column('place_id', String(60), ForeignKey('places.id'), primary_key=True)
    )

    # Establish relationship only if using DBStorage
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        places = relationship(
            "Place",
            secondary=place_amenity,
            back_populates="amenities"
        )
