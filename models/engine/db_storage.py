#!/usr/bin/python3
""" DB Storage Module """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base


class DBStorage:
    """ Database storage class """

    __engine = None
    __session = None

    def __init__(self):
        """ Initializes the DBStorage instance """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        if cls:
            return {obj.id: obj for obj in self.__session.query(cls).all()}
        else:
            classes = [State, City]  # Extend this list with other classes
            objs = {}
            for cls in classes:
                objs.update(self.all(cls))
            return objs

    def new(self, obj):
        """ Adds the object to the current database session """

        if obj:
            self.__session.add(obj)

    def save(self):
        """ Commits all changes of the current database session """

        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes obj from the current database session """

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables in the database """

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Calls remove() on the private session attribute """

        self.__session.remove()
