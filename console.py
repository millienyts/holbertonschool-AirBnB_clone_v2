#!/usr/bin/python3
import cmd
import sys
import json
import uuid
from datetime import datetime
from os import getenv
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
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
        if not ('.' in line and '(' in line and ')' in line):
            return line
        try:
            pline = line[:]
            _cls = pline[:pline.find('.')]
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                pline = pline.partition(', ')
                _id = pline[0].replace('\"', '')
                if pline[2]:
                    if pline[2][0] == '{' and pline[2][-1] == '}' and type(eval(pline[2])) is dict:
                        _args = pline[2]
                    else:
                        _args = pline[2].replace(',', '')
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
        att_dict = {}

        if not args:
            print("** class name missing **")
            return

        args = args.partition(" ")
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

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

    def help_create(self):
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
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
        else:
            key = c_name + '.' + c_id
            if key in storage.all():
                storage.all().pop(key)
                storage.save()
            else:
                print("** no instance found **")

    def help_destroy(self):
        print("Deletes an instance based on the class name and id")
        print("[Usage]: destroy <className> <instanceId>\n")

if __name__ == '__main__':
    HBNBCommand().cmdloop()

