#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from models.city import City
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class"""
    __tablename__ = 'states'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        name = ""

        @property
        def cities(self):
            """ Returns a list of City instances where the state_id
                matches the id of the current State,leveraging
                the FileStorage relationship between State and City
            """
            from models import storage
            associated_cities = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    associated_cities.append(city)
            return associated_cities
