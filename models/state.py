#!/usr/bin/python3
""" State Module """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ Defines the State class """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship("City", back_populates="state")
