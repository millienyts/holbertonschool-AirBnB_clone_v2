#!/usr/bin/python3
'''
This is the console for the AirBnB clone project.
It is used to manage the objects of your project:
    - Create a new object (ex: a new User or a new Place)
    - Retrieve an object from the file storage
    - Perform operations on objects (count, compute stats, etc.)
    - Update attributes of an object
    - Destroy an object
'''
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from shlex import split

class HBNBCommand(cmd.Cmd):
    '''
    AirBnB console class
    '''
    prompt = '(hbnb) '
    classes = {"BaseModel", "User", "State", "City", "Amenity", "Place", "Review"}

    def emptyline(self):
        '''Empty line'''
        pass

    def do_quit(self, line):
        '''Quit command to exit the program'''
        return True

    def do_EOF(self, line):
        '''EOF command to exit the program'''
        print()
        return True

    def do_create(self, line):
        '''Creates a new instance of BaseModel'''
        args = split(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(args[0])()
            new_instance.save()
            print(new_instance.id)

    def help_create(self):
        '''Help for create command'''
        print("Creates a new instance of BaseModel.")
        print("Usage: create <class name>")

    def do_show(self, line):
        '''Prints the string representation of an instance'''
        args = split(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + '.' + args[1]
            if key in storage.all():
                print(storage.all()[key])
            else:
                print("** no instance found **")

    def help_show(self):
        '''Help for show command'''
        print("Prints the string representation of an instance")
        print("Usage: show <class name> <instance id>")

    def do_destroy(self, line):
        '''Deletes an instance based on the class name and id'''
        args = split(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + '.' + args[1]
            if key in storage.all():
                del storage.all()[key]
                storage.save()
            else:
                print("** no instance found **")

    def help_destroy(self):
        '''Help for destroy command'''
        print("Deletes an instance based on the class name and id")
        print("Usage: destroy <class name> <instance id>")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
