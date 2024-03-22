#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship("City", backref="state",
                          cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.save()

    @property
    def cities(self):
        """
        Getter for cities related to a state using a FIlEStorage engine
        """
        from models import storage
        st_cities = []
        for city in storage.all(City).values():
            if (self.id == city.state_id):
                st_cities.append(city)
        return st_cities
