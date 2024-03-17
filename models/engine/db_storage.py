#!/usr/bin/python3
"""DBStorage class definition"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DBStorage:
    """ Database storage class encapsulating SQLAlchemy session management """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DBStorage instance"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session based on class name"""
        objs = {}
        if cls:
            if type(cls) == str:
                cls = eval(cls)
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objs[key] = obj
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for cls in classes:
                cls_objs = self.__session.query(cls).all()
                for obj in cls_objs:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objs[key] = obj
        return objs

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and initializes a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Calls remove() on the private session attribute, ending the session"""
        self.__session.close()
