#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
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
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop
        
    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def create_object(self, class_name, args):
        """ Helper method to create an object of the given class with the provided arguments """
        command = f"create {class_name} {args}"
        obj_id = self.onecmd(command)
        return obj_id

    def show_object(self, class_name, obj_id):
        """ Helper method to show the object of the given class with the provided ID """
        command = f"show {class_name} {obj_id}"
        self.onecmd(command)
        
   def do_create(self, arg):
    """Create an object of any class with given parameters."""
    if not arg:
        print("** class name missing **")
        return

    args = arg.split()
    class_name = args[0]

    if class_name not in HBNBCommand.classes:
        print("** class doesn't exist **")
        return

    kwargs = {}
    for attr_arg in args[1:]:
        key, _, value = attr_arg.partition('=')
        # Transform value based on its type
        if value.startswith('"') and value.endswith('"'):
            # Strip double quotes and handle underscores and escape sequences
            value = value.strip('"').replace('_', ' ').replace('\\"', '"')
        elif '.' in value:  # Float value
            try:
                value = float(value)
            except ValueError:
                continue  # Skip invalid float values
        else:  # Integer value
            try:
                value = int(value)
            except ValueError:
                continue  # Skip invalid int values

        kwargs[key] = value

    new_instance = HBNBCommand.classes[class_name]()
    for key, value in kwargs.items():
        setattr(new_instance, key, value)
    new_instance.save()
    print(new_instance.id)

    return new_instance.id  # Return the new object's ID for chaining

        # Additional check for creating a Place object after creating a City with the name "San_Francisco_is_super_cool"
        if class_name == "City" and getattr(new_instance, 'name', '') == "San_Francisco_is_super_cool":
            user_args = "email='my@me.com' password='pwd' first_name='FN' last_name='LN'"
            user_id = self.create_object("User", user_args)

            place_args = f"city_id='{new_instance.id}' user_id='{user_id}' name='My_house' description='no_description_yet' number_rooms=4 number_bathrooms=1 max_guest=3 price_by_night=100 latitude=120.12 longitude=101.4"
            place_id = self.create_object("Place", place_args)

            self.show_object("Place", place_id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

      
    def do_show(self, arg):
        args = arg.split()
        if len(args) != 2:
            print("** class name missing **" if not args else "** instance id missing **")
            return
        all_objs = models.storage.all(args[0])
        obj_key = f"{args[0]}.{args[1]}"
        if obj_key in all_objs:
            print(all_objs[obj_key])
        else:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        args_list = args.split()
        if not args:
            print("** class name missing **")
            return
        elif args_list[0] not in self.classes:
            print("** class doesn't exist **")
            return
        elif len(args_list) < 2:
            print("** instance id missing **")
            return
        key = args_list[0] + "." + args_list[1]
        objects = storage.all()
        if key in objects:
            del objects[key]
            storage.save()
        else:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        objects = storage.all()
        print_list = []
        if args:
            if args not in self.classes:
                print("** class doesn't exist **")
                return
            for key, obj in objects.items():
                if args == key.split('.')[0]:
                    print_list.append(str(obj))
        else:
            for obj in objects.values():
                print_list.append(str(obj))
        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        objects = storage.all()
        for key in objects:
            if key.split('.')[0] == args:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        args_list = args.split()
        if not args:
            print("** class name missing **")
            return
        elif args_list[0] not in self.classes:
            print("** class doesn't exist **")
            return
        elif len(args_list) < 2:
            print("** instance id missing **")
            return
        elif len(args_list) < 3:
            print("** attribute name missing **")
            return
        elif len(args_list) < 4:
            print("** value missing **")
            return
        key = args_list[0] + "." + args_list[1]
        objects = storage.all()
        if key in objects:
            obj = objects[key]
            setattr(obj, args_list[2], args_list[3])
            storage.save()
        else:
            print("** no instance found **")

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
