from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models import storage

Base = declarative_base()


class BaseModel:
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        for key, value in kwargs.items():
            if key != '__class__':
                setattr(self, key, value)

    def save(self):
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def delete(self):
        storage.delete(self)

    def to_dict(self):
        dictionary = {**self.__dict__}
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = dictionary['created_at'].isoformat()
        dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    @classmethod
    def close(cls):
        """Calls remove() method(if DBStorage)."""
        from models import storage  # Import moved inside the method
        storage.close()
