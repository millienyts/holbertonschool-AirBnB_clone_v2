import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models import get_storage

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models."""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model."""
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        for key, value in kwargs.items():
            if key != '__class__':
                setattr(self, key, value)

    def save(self):
        """Saves the instance to storage."""
        self.updated_at = datetime.utcnow()
        storage = get_storage()
        storage.new(self)
        storage.save()

    def delete(self):
        """Deletes the instance from storage."""
        storage = get_storage()
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format."""
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        if '_sa_instance_state' in my_dict:
            del my_dict['_sa_instance_state']
        my_dict['created_at'] = my_dict['created_at'].isoformat()
        my_dict['updated_at'] = my_dict['updated_at'].isoformat()
        return my_dict

    @classmethod
    def close(cls):
        """Call remove() method on the private (if DBStorage)."""
        from models import storage
        storage.close()
