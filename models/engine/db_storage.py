#!/usr/bin/python3
"""database storage engine"""

from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import os
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, scoped_session


class DBStorage:
    """database storage enginee"""
    __engine = None
    __session = None

    def __init__(self):
        """instantiation of dbstorage"""
        self.__engine = create_engine(f"mysql+mysqldb://"
                                      + f"{os.getenv('HBNB_MYSQL_USER')}:"
                                      + f"{os.getenv('HBNB_MYSQL_PWD')}"
                                      + f"@{os.getenv('HBNB_MYSQL_HOST')}/"
                                      + f"{os.getenv('HBNB_MYSQL_DB')}",
                                      pool_pre_ping=True)

        if os.getenv("HBNB_MYSQL_USER") == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        dict = {}

        if cls is None:
            objects_list = self.__session.query(State).all()
            objects_list.extend(self.__session.query(City).all())
            objects_list.extend(self.__session.query(User).all())
            objects_list.extend(self.__session.query(Place).all())
            objects_list.extend(self.__session.query(Review).all())
            objects_list.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objects_list = self.__session.query(cls).all()

        for obj in objects_list:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            dict[key] = obj

        return dict

    def new(self, obj):
        """add an obj to the current database session"""
        # self.__session.add(obj)
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes from the current database session the obj
            if not None
        """
        # if obj is not None:
        # self.__session.query(type(obj)).filter(
        # type(obj).id == obj.id).delete()
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """initialise a database session"""
        Base.metadata.create_all(self.__engine)
        _session = sessionmaker(bind=self.__engine,
                                expire_on_commit=False)
        self.__session = scoped_session(_session)

    def close(self):
        """closing current session"""
        self.__session.remove()

    def close(self):
        """
        Closes Session
        """
        self.__session.close()
