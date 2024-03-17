#!/usr/bin/python3
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.place import Place

class City(BaseModel, Base):
    """Represents a City in the database.

    This class links to the 'cities' table and includes relationships to other models, such as Place.

    Attributes:
        name (sqlalchemy.Column): The city name.
        state_id (sqlalchemy.Column): Foreign key linking a city to its state.
    """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    # Establishes a relationship with the 'Place' model, enabling access to associated places within a city.
    places = relationship('Place', cascade='all, delete, delete-orphan', backref='cities')
