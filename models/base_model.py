import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all HBNB models."""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a new model."""
        self.id = kwargs.get('id', str(uuid.uuid4()))
        now = datetime.utcnow()
        self.created_at = kwargs.get('created_at', now)
        self.updated_at = kwargs.get('updated_at', now)

        for key, value in kwargs.items():
            if key not in ('id', 'created_at', 'updated_at', '__class__'):
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        from models import storage
        storage.new(self)
        storage.save()

    def delete(self):
        """Delete the current instance from the storage"""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Converts instance into dict format for serialization."""
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        if '_sa_instance_state' in my_dict:
            del my_dict['_sa_instance_state']
        # Ensure created_at and updated_at are datetime objects
        for key in ['created_at', 'updated_at']:
            if isinstance(my_dict[key], datetime):
                my_dict[key] = my_dict[key].isoformat()
        return my_dict

    @classmethod
    def close(cls):
        """Calls remove() method(if DBStorage)."""
        from models import storage  # Import moved inside the method
        storage.close()
