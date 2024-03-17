#!/usr/bin/python3

import cmd
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary to map class names to their corresponding classes
entity_classes = {
    "Amenity": Amenity, 
    "BaseModel": BaseModel, 
    "City": City,
    "Place": Place, 
    "Review": Review, 
    "State": State, 
    "User": User
}

class CustomHBNBCommand(cmd.Cmd):
    """ Custom HBNB Command Line Interface """
    prompt = '(custom_hbnb) '

    def do_end(self, argument):
        """Exits the console with End command"""
        return True

    def ignore_empty(self):
        """Prevents execution of empty commands"""
        return False

    def do_exit(self, argument):
        """Command to exit the CLI gracefully"""
        return True

    def parse_key_values(self, arguments):
        """Converts key=value pairs into a dictionary"""
        parsed_dict = {}
        for arg in arguments:
            if "=" in arg:
                key, value = arg.split('=', 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value.strip('"').replace('_', ' ')
                else:
                    try:
                        value = eval(value)
                    except:
                        continue
                parsed_dict[key] = value
        return parsed_dict

    def do_initialize(self, arguments):
        """Creates an instance of a specified class"""
        args = arguments.split()
        if not args:
            print("** Missing class name **")
            return False
        if args[0] in entity_classes:
            init_dict = self.parse_key_values(args[1:])
            instance = entity_classes[args[0]](**init_dict)
        else:
            print("** Class does not exist **")
            return False
        print(instance.id)
        instance.save()

    def do_present(self, arguments):
        """Displays a specific instance based on class and id"""
        args = shlex.split(arguments)
        if not args:
            print("** Missing class name **")
            return False
        if args[0] in entity_classes:
            if len(args) > 1:
                identifier = f"{args[0]}.{args[1]}"
                if identifier in models.storage.all():
                    print(models.storage.all()[identifier])
                else:
                    print("** Instance not found **")
            else:
                print("** Missing instance ID **")
        else:
            print("** Class does not exist **")

    def do_remove(self, arguments):
        """Deletes a specific instance"""
        args = shlex.split(arguments)
        if not args:
            print("** Missing class name **")
        elif args[0] in entity_classes:
            if len(args) > 1:
                identifier = f"{args[0]}.{args[1]}"
                if identifier in models.storage.all():
                    del models.storage.all()[identifier]
                    models.storage.save()
                else:
                    print("** Instance not found **")
            else:
                print("** Missing instance ID **")
        else:
            print("** Class does not exist **")

    def do_list_all(self, arguments):
        """Lists all instances of a class or all classes if no class is specified"""
        args = shlex.split(arguments)
        if not args:
            obj_dict = models.storage.all()
        elif args[0] in entity_classes:
            obj_dict = models.storage.all(entity_classes[args[0]])
        else:
            print("** Class does not exist **")
            return False
        print([str(obj) for obj in obj_dict.values()])

    def do_modify(self, arguments):
        """Updates an instance with new information"""
        args = shlex.split(arguments)
        if not args:
            print("** Missing class name **")
        elif args[0] in entity_classes:
            if len(args) > 2:
                identifier = f"{args[0]}.{args[1]}"
                if identifier in models.storage.all():
                    instance = models.storage.all()[identifier]
                    if args[2] in ("number_rooms", "number_bathrooms", "max_guest", "price_by_night"):
                        value = int(args[3]) if args[3].isdigit() else 0
                    elif args[2] in ("latitude", "longitude"):
                        value = float(args[3]) if '.' in args[3] else 0.0
                    else:
                        value = args[3]
                    setattr(instance, args[2], value)
                    instance.save()
                else:
                    print("** Instance not found **")
            else:
                print("** Missing attribute name or value **")
        else:
            print("** Class does not exist **")


if __name__ == '__main__':
    CustomHBNBCommand().cmdloop()
