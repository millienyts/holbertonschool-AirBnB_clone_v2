#!/usr/bin/python3
"""Defines tests for the HBNB console."""
import unittest
from unittest.mock import patch
from io import StringIO
import pep8
import os
import console
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
import models

class TestConsole(unittest.TestCase):
    """Tests the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """Prepare test environment."""
        cls.console = HBNBCommand()
        FileStorage._FileStorage__objects = {}
        if os.path.exists("file.json"):
            os.rename("file.json", "temp_file.json")

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        del cls.console
        if os.path.exists("temp_file.json"):
            os.rename("temp_file.json", "file.json")
        if type(models.storage) == DBStorage:
            models.storage._DBStorage__session.close()

    def setUp(self):
        """Runs before each test."""
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Runs after each test."""
        try:
            os.remove("file.json")
        except Exception:
            pass
            
   def test_create_command(self):
        """Test 'create' command adds new instance to FileStorage."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('sys.stdin', new_callable=StringIO) as mock_stdin:
                mock_stdin.write('create BaseModel\n')
                mock_stdin.seek(0)
                HBNBCommand().onecmd('create BaseModel')
                output = mock_stdout.getvalue().strip()
                self.assertTrue(len(output) > 0)
                # Check if the created ID exists in storage
                all_objs = storage.all()
                obj_exists = any(['BaseModel.' + output in key for key in all_objs.keys()])
                self.assertTrue(obj_exists)

    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors (and warnings).")

    def test_docstrings_presence(self):
        """Test for the presence of docstrings in the console module."""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_empty_line(self):
        """Test that an empty line plus ENTER executes nothing."""
        with patch('sys.stdout', new_callable=StringIO) as mock_output:
            self.console.onecmd("\n")
            self.assertEqual('', mock_output.getvalue())

    def test_quit_command(self):
        """Test the quit command exits the program."""
        with patch('sys.stdout', new_callable=StringIO) as mock_output:
            self.assertTrue(self.console.onecmd("quit"))

    def test_EOF_command(self):
        """Test the EOF command exits the program."""
        with patch("sys.stdout", new_callable=StringIO) as mock_output:
            self.assertTrue(self.console.onecmd("EOF"))

    def test_create_errors(self):
        """Test create command errors."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.consol.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
            with patch("sys.stdout", new=StringIO()) as f:
                self.consol.onecmd("create asdfsfsd")
                self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBS")
    def test_create(self):
        """Test create command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create BaseModel")
            BaseM = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
            usr = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Place")
            plc = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create City")
            cty = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create State")
            ste = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Amenity")
            amn = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Review")
            rew = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Place")
            plc = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            self.assertIn(usr, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all BaseModel")
            self.assertIn(BaseM, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all State")
            self.assertIn(ste, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all City")
            self.assertIn(cty, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Place")
            self.assertIn(plc, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Review")
            self.assertIn(rew, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all Amenity")
            self.assertIn(amn, f.getvalue())


    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBS")
    def test_kwargs(self):
        with patch("sys.stdout", new=StringIO()) as f:
            get = ("create Place city_id='001' name='My_little_house' "
                   "number_rooms=5 latitude=37.77 longitude=a")
            self.consol.onecmd(get)
            plc = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.consol.onecmd("all Place")
            out = f.getvalue()
            self.assertIn("'city_id': '001'", out)
            self.assertIn("'name': 'My_little_house'", out)
            self.assertIn("'number_rooms': 5", out)
            self.assertIn("'latitude': 37.77", out)
            self.assertNotIn("'longitude'", out)

    def test_show(self):
        """Test show command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBS")
    def test_all(self):
        """Test all command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBS")
    def test_update(self):
        """Test update command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBS")
    def test_z_all(self):
        """Test alternate all command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("asdfsdfsd.all()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("State.all()")
            self.assertEqual("[]\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBS")
    def test_z_count(self):
        """Test count command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("asdfsdfsd.count()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("State.count()")
            self.assertEqual("0\n", f.getvalue())

    def test_z_show(self):
        """Test alternate show command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("safdsa.show()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("BaseModel.show(abcd-123)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("Galaxy.destroy()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.destroy(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBS")
    def test_update(self):
        """Test alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("sldkfjsl.update()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + my_id + ")")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + my_id + ", name)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

if __name__ == "__main__":
    unittest.main()
