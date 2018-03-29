#!/usr/bin/python3
''' Test suite for the console'''


import sys
import os
import models
import unittest
from io import StringIO
from console import HBNBCommand
from unittest.mock import create_autospec
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


class test_console(unittest.TestCase):
    ''' Test the console module'''
    def setUp(self):
        '''setup for'''
        self.backup = sys.stdout
        self.capt_out = StringIO()
        sys.stdout = self.capt_out

    def tearDown(self):
        ''''''
        sys.stdout = self.backup

    def create(self):
        ''' create an instance of the HBNBCommand class'''
        return HBNBCommand()

    def test_quit(self):
        ''' Test quit exists'''
        console = self.create()
        self.assertTrue(console.onecmd("quit"))

    def test_EOF(self):
        ''' Test EOF exists'''
        console = self.create()
        self.assertTrue(console.onecmd("EOF"))

    def test_all(self):
        ''' Test all exists'''
        console = self.create()
        console.onecmd("all")
        self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    def test_show(self):
        '''
            Testing that show exists
        '''
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            console = self.create()
            console.onecmd("create User name=\"John\" email=\"x@x.com\"")
            user_id = self.capt_out.getvalue()
            sys.stdout = self.backup
            self.capt_out.close()
            self.capt_out = StringIO()
            sys.stdout = self.capt_out
            console.onecmd("show User " + user_id)
            x = (self.capt_out.getvalue())
            sys.stdout = self.backup
            self.assertTrue(str is type(x))

    def test_show_class_name(self):
        '''
            Testing the error messages for class name missing.
        '''
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd("show")
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual("** class name missing **\n", x)

    def test_show_class_name(self):
        '''
            Test show message error for id missing
        '''
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd("show User")
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual("** instance id missing **\n", x)

    def test_show_no_instance_found(self):
        '''
            Test show message error for id missing
        '''
        console = self.create()
        console.onecmd("create user")
        user_id = self.capt_out.getvalue()
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        console.onecmd("show User " + "124356876")
        x = (self.capt_out.getvalue())
        sys.stdout = self.backup
        self.assertEqual("** no instance found **\n", x)

    def test_create(self):
        '''
            Test that create works
        '''
        console = self.create()
        console.onecmd("create User")
        self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    def test_model_with_kwargs_gets_attributes_set(self):
        '''
            Test that a model's attributes get set in db if keyword args are
            supplied.
        '''
        if (os.getenv('HBNB_TYPE_STORAGE') == 'db'):
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            from sqlalchemy.ext.declarative import declarative_base
            user = os.getenv('HBNB_MYSQL_USER')
            password = os.getenv('HBNB_MYSQL_PWD')
            host = os.getenv('HBNB_MYSQL_HOST')
            database = os.getenv('HBNB_MYSQL_DB')

            # Request a connection with the database once required
            self.engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                          format(user, password, host, database),
                                          pool_pre_ping=True)
            Base = declarative_base()
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            Base.metadata.create_all(self.engine)
            console = self.create()
            console.onecmd("create State name='California'")
            user_id = self.capt_out.getvalue()
            sys.stdout = self.backup
            self.capt_out.close()
            from models.state import State
            query = self.session.query(State).all()
            self.assertEqual('California', user_id)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 'filestorage' +
                     'engine doesn\'t need kwargs')
    def test_create_adds_parameters_to_instances_attributes(self):
        '''
            Testing that do_create adds parameters to the instance's attrs
        '''
        console = self.create()
        console.onecmd("create BaseModel name=\"Holly\"")
        console.onecmd("all")
        x = (self.capt_out.getvalue())
        self.assertEqual('Holly' in x, True)

    def test_class_name(self):
        '''
            Testing the error messages for class name missing.
        '''
        console = self.create()
        console.onecmd("create")
        x = (self.capt_out.getvalue())
        self.assertEqual("** class name missing **\n", x)

    def test_class_name_doest_exist(self):
        '''
            Testing the error messages for class name missing.
        '''
        console = self.create()
        console.onecmd("create Binita")
        x = (self.capt_out.getvalue())
        self.assertEqual("** class doesn't exist **\n", x)
