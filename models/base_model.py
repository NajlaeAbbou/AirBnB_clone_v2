#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from models import storage_type
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models
    Attributes:
        id : The BaseModel id
        created_at : The datetime at creation
        updated_at : The datetime of last update
    """
    id = Column(String(60),
                nullable=False,
                primary_key=True,
                unique=True)
    created_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
        else:
            for k in kwargs:
                if k in ['created_at', 'updated_at']:
                    setattr(self, k, datetime.fromisoformat(kwargs[k]))
                elif k != '__class__':
                    setattr(self, k, kwargs[k])

            if not hasattr(kwargs, 'id'):
                self.id = str(uuid.uuid4())
            if not hasattr(kwargs, 'created_at'):
                self.created_at = datetime.now()
            if not hasattr(kwargs, 'updated_at'):
                self.updated_at = self.created_at

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        for k in dictionary:
            if type(dictionary[k]) is datetime:
                dictionary[k] = dictionary[k].isoformat()
        if '_sa_instance_state' in dictionary.keys():
            del(dictionary['_sa_instance_state'])
        return dictionary

    def delete(self):
        '''deletes the current instance from the storage'''
        from models import storage
        storage.delete(self)
