#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel

# Create a new object and save
obj = BaseModel()
obj.name = "Test Object"
obj.my_number = 89
obj.save()

# Simulate relaunching the program and reloading objects
storage.reload()

# Access reloaded objects
reloaded_objs = storage.all()
for obj_id, obj in reloaded_objs.items():
    print(obj)

