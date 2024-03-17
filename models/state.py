#!/usr/bin/python3
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models

class State(BaseModel, Base):
    """
    A representation of a state within the AirBnB clone platform.
    
    States are used to organize places into larger geographical areas, making it easier for users to find accommodations.

    Attributes:
        name (Column): The name of the state.
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    # Relationship with the City model, including cascading options to maintain integrity.
    cities = relationship("City", cascade='all, delete, delete-orphan', backref="state")

    @property
    def cities(self):
        """
        A property that overrides the cities relationship in file storage mode.
        
        This custom property dynamically gathers all City instances from file storage that belong to the current State.
        """
        all_cities = models.storage.all(models.City)
        # Filter and return cities that belong to this state.
        return [city for city in all_cities.values() if city.state_id == self.id]
