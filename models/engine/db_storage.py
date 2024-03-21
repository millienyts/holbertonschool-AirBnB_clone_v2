#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        environ = getenv("HBNB_ENV")  # Integrated from code 1

        db_url = f"mysql+mysqldb://{user}:{pwd}@{host}:3306/{db}"
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if environ == 'test':  # Logic from code 1 integrated
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a specific class or all classes if cls=None."""
        objs = {}
        if cls:
            cls = DBStorage.classes().get(cls, cls)  # Dynamic class resolution
            objs.update({f'{type(obj).__name__}.{
                        obj.id}': obj for obj in self.__session.query(cls).all()})
        else:
            for cls in Base.__subclasses__():
                cls_name = cls.__name__
                objs.update(
                    {f'{cls_name}.{obj.id}': obj for obj in self.__session.query(cls).all()})
        return objs

    def new(self, obj):
        """Add the object to the current database session."""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None."""
        if obj:
            # Unified delete method, keeping it simple.
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the session."""
        self.__session.close()

    @staticmethod
    def classes():
        """Return a dictionary of all classes available."""
        return {
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
