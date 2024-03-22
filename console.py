#!/usr/bin/python3
import cmd
import sys
<<<<<<< HEAD
import json
import uuid
from datetime import datetime
from os import getenv
=======
import shlex
>>>>>>> 94700d9aa78df0e8136cc9ea920f018e9aaccfb9
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os
os.environ['HBNB_TYPE_STORAGE'] = 'file'


class HBNBCommand(cmd.Cmd):
<<<<<<< HEAD
=======
    """Contains the functionality for the HBNB console"""

    # Determines prompt for interactive/non-interactive modes
>>>>>>> 94700d9aa78df0e8136cc9ea920f018e9aaccfb9
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
<<<<<<< HEAD
=======
        """Reformat command line for advanced command syntax."""
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formatting - i.e '.', '(', ')'
>>>>>>> 94700d9aa78df0e8136cc9ea920f018e9aaccfb9
        if not ('.' in line and '(' in line and ')' in line):
            return line
        try:
            pline = line[:]
            _cls = pline[:pline.find('.')]
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception
<<<<<<< HEAD
=======

            # if parentheses contain arguments, parse them
>>>>>>> 94700d9aa78df0e8136cc9ea920f018e9aaccfb9
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                pline = pline.partition(', ')
                _id = pline[0].replace('\"', '')
<<<<<<< HEAD
                if pline[2]:
                    if pline[2][0] == '{' and pline[2][-1] == '}' and type(eval(pline[2])) is dict:
                        _args = pline[2]
                    else:
                        _args = pline[2].replace(',', '')
=======

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')

>>>>>>> 94700d9aa78df0e8136cc9ea920f018e9aaccfb9
            line = ' '.join([_cmd, _cls, _id, _args])
        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        exit()

    def help_quit(self):
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        print()
        exit()

    def help_EOF(self):
        print("Exits the program without formatting\n")

    def emptyline(self):
        pass

    def do_create(self, args):
<<<<<<< HEAD
        att_dict = {}

        if not args:
=======
        """Create an object of any class."""
        args_list = shlex.split(args)
        if len(args_list) == 0:
>>>>>>> 94700d9aa78df0e8136cc9ea920f018e9aaccfb9
            print("** class name missing **")
            return

        class_name = args_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

<<<<<<< HEAD
        if args[2]:
            parameters = args[2]
            parameters = parameters.split(" ")[:]
            id = str(uuid.uuid4())

            att_dict['id'] = id

            if getenv("HBNB_TYPE_STORAGE") == "db":
                att_dict['created_at'] = datetime.utcnow().isoformat()
                att_dict['updated_at'] = datetime.utcnow().isoformat()
            else:
                att_dict['created_at'] = datetime.now().isoformat()
                att_dict['updated_at'] = datetime.now().isoformat()

            att_dict['__class__'] = str(args[0])

            for parameter in parameters:
                att_name = parameter.partition("=")[0]
                sign = parameter.partition("=")[1]
                att_value = parameter.partition("=")[2]

                if sign and att_value:
                    if att_value.startswith('\"') and not att_value.endswith('\"'):
                        pass
                    elif not att_value.startswith('\"') and att_value.endswith('\"'):
                        pass
                    else:
                        att_value = att_value.replace('_', ' ')
                        if '"' in att_value:
                            att_value = att_value[1:-1]
                            att_value = str(att_value)
                        elif '.' in att_value:
                            att_value = float(att_value)
                        else:
                            att_value = int(att_value)

                    att_dict[att_name] = att_value

        new_instance = HBNBCommand.classes[args[0]](**att_dict)
        new_instance.save()
        print(new_instance.id)
=======
        # User-specific validation and creation logic
        if class_name == "User":
            # Extract and validate user-specific attributes
            email = None
            password = None
            for arg in args_list[1:]:
                key, value = arg.split("=", 1)
                if key == "email":
                    email = value.strip("\"")
                elif key == "password":
                    password = value.strip("\"")

            # Check for required attributes
            if not email or not password:
                print("** User object requires email and password **")
                return

            # Create User instance with required and optional attributes
            user_instance = User(email=email, password=password)
            for arg in args_list[1:]:
                key, value = arg.split("=", 1)
                # Skip email and password as they're already set
                if key in ["first_name", "last_name"]:
                    setattr(user_instance, key, value.strip("\""))

            user_instance.save()
            print(user_instance.id)
            storage.new(user_instance)
            storage.save()
            return

        # General object creation logic for other classes
        kwargs = {}
        for arg in args_list[1:]:
            try:
                key, value = arg.split("=", 1)
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1].replace('_', ' ').replace('\\"', '"')
                elif '.' in value:
                    value = float(value)
                else:
                    value = int(value)
                kwargs[key] = value
            except ValueError:
                continue  # Skip invalid format

        # Create the instance for other classes
        instance = self.classes[class_name](**kwargs)
        instance.save()
        print(instance.id)
        storage.new(instance)
        storage.save()

    def validate_state_id(self, state_id):
        """Validate the existence of state_id in the storage."""
        states = self.classes['State'].all()
        return any(state.id == state_id for state in states.values())

    def validate_city_state_id(self, state_id):
        """Validate the existence of state_id in DB or file storage."""
        # Implementation depends on the storage system in use
        # This is a placeholder function;
        return True
    # Add or modify other methods as necessary...

    def validate_city_user_ids(self, city_id, user_id):
        """Validates the existence of city_id and user_id."""
        city_exists = storage.get(
            "City", city_id) is not None if city_id else True
        user_exists = storage.get(
            "User", user_id) is not None if user_id else True
        if not city_exists or not user_exists:
            print("** city_id or user_id does not exist **")
            return False
        return True

    def extract_place_args(self, args_list):
        """Extracts and returns city_id and user_id from args_list."""
        city_id = user_id = None
        for arg in args_list:
            if arg.startswith("city_id="):
                city_id = arg.split("=", 1)[1].strip('"')
            elif arg.startswith("user_id="):
                user_id = arg.split("=", 1)[1].strip('"')
        return city_id, user_id

    def check_existence(self, key, value):
        """Stub for checking if the given key-value exists in storage."""
        # Implement the actual check here, depending on your storage system
        # For now, let's assume everything exists
        return True
>>>>>>> 94700d9aa78df0e8136cc9ea920f018e9aaccfb9

    def help_create(self):
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
<<<<<<< HEAD
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

                if not c_name:
            print("** class name missing **")
        elif c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif not c_id:
            print("** instance id missing **")
        else:
            key = c_name + '.' + c_id
            if key in storage.all():
                print(storage.all()[key])
            else:
                print("** no instance found **")
=======
        """Method to show an individual object"""
        args_list = shlex.split(args)
        if len(args_list) == 0:
            print("** class name missing **")
            return
        if len(args_list) == 1:
            print("** instance id missing **")
            return
        class_name, id = args_list[:2]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        all_objs = storage.all(self.classes[class_name])
        key = f"{class_name}.{id}"
        if key in all_objs:
            print(all_objs[key])
        else:
            print("** no instance found **")
>>>>>>> 94700d9aa78df0e8136cc9ea920f018e9aaccfb9

    def help_show(self):
        print("Prints the string representation of an instance")
        print("[Usage]: show <className> <instanceId>\n")

    def do_destroy(self, args):
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        if not c_name:
            print("** class name missing **")
        elif c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif not c_id:
            print("** instance id missing **")
<<<<<<< HEAD
        else:
            key = c_name + '.' + c_id
            if key in storage.all():
                storage.all().pop(key)
                storage.save()
            else:
                print("** no instance found **")
=======
            return

        key = c_name + "." + c_id

        try:
            del (storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        # print(args)
        # return
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")
>>>>>>> 94700d9aa78df0e8136cc9ea920f018e9aaccfb9

    def help_destroy(self):
        print("Deletes an instance based on the class name and id")
        print("[Usage]: destroy <className> <instanceId>\n")

if __name__ == '__main__':
    HBNBCommand().cmdloop()

