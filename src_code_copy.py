# phython pure abstract superclass / interface for runer objects
from Imodel import Model
from create_uml import Uml
from python_to_dot import Dot_file
from Command import CommandLineInterface
from connect_to_database import Database_connector
from cmd import Cmd
from os import path
import doctest  # not doing much yet
import sqlite3  # database interactions
import json
from subprocess import call
from os.path import abspath, split
from sys import argv
from subprocess import call as sub_call
from json import load
from shlex import split
from os import system
from os.path import abspath, split as os_split
import graphviz
from pylint import pyreverse
from abc import ABC, abstractmethod


class Model(ABC):

    def run(self):
        pass


class Uml(Model):

    def __init__(self):
        super().__init__()
        self.error = ""

    def run(self):
        self.main()

    def get_result(self):
        return self.error

    def json_extract(self, component='db_commands'):
        with open('config.json') as config:
            result = load(config)
            result = result[component]
        return result

    def main(self):
        script_path = abspath(__file__)
        script_dir = os_split(script_path)[0]
        system('cd ' + script_dir)
        dot_file_path = (script_dir + "\\" +
                         self.json_extract('paths')['dot.exe'])
        destination_file = self.json_extract('paths')['dot_file']
        args = ""
        if argv.__len__() < 2:
            args = '-Tpng -omy_classes.png'

        else:
            for arg in argv[1:]:
                args += arg
                self.error += arg
        ar = [dot_file_path]+[destination_file] + split(args)
        try:
            sub_call(ar)
            self.error += 'uml created'
        except(PermissionError):
            self.error += "you don't Hve valid permissions to create this file"
        except(FileNotFoundError):
            self.error += "cannot find file at " + ar


class Dot_file(Model):

    def __init__(self):
        Model().__init__()
        self.error = ""

    def run(self):
        args = split(self.json_extract('paths')['source_code'])
        self.error += str(self.create_dot_file(args))

    def json_extract(self, component='db_commands'):
        with open('config.json') as config:
            result = load(config)
            result = result[component]
        return result

    def create_dot_file(self, args):
        try:  # reads, analyses, and creates .dot file from the destination file
            call(['pyreverse'] + args)
        except ValueError as e:  # if not, gives error message
            return('there was a problem converting the .py file with pyreverse', e)


# get path to config file

# read config file


class Database_connector(Model):
    # intake string of database name
    # if no name, set database name to be json_extract('db_commands'['db'])
    # create database

    def __init__(self):
        super().__init__()
        doctest.testmod()
        self.error = ""

    def run(self):
        self.connection = self.connect()
        self.make_tables()
        data = self.select_from_sql()
        self.error = "the data in the database is :\n"
        if(data.__len__() > 1):
            self.error += str(data)
            self.error += "\ndatabase complete"
        else:
            self.error += str(data)
            self.error += "the database is empty"

    def get_result(self):
        return self.error

    def connect(self, db=None):
        '''
        >>> type(connect())
        <class 'sqlite3.Connection'>

        '''
        connection = None
        #  assert(db is None)
        if (db is None):
            js = self.json_extract()
            db = js['db']

        try:
            connection = sqlite3.connect(db)
        except():
            self.error += "error at creating database"
        return connection

    def json_extract(self, component='db_commands'):
        '''
        make sure that the method gets a dictionary from json by default
        >>> type(json_extract())
        <class 'dict'>

        >>> json_extract('json_test')
        {'item_one': 'one', 'item_two': 'two'}

        >>> json_extract('bad_data')
        bad_data does not exist in config file
        '''

        result = None
        try:
            with open('config.json') as config:
                whole_file = json.load(config)
                result = whole_file[component]
        except(KeyError):
            self.error += component + " does not exist in config file"
        return result

    # uses regex to read a dot file, and creates tables from data

    def make_tables(self):
        '''
        >>> make_tables()
        Traceback (most recent call last):
        File "%\\doctest.py", line 1329, in __run
            compileflags, 1), test.globs)
        File "<doctest __main__.make_tables[0]>", line 1, in <module>
            make_tables()
        TypeError: make_tables() missing 1 required positional argument:\
    'connection'


        '''
        ##
        # get file to extract data from
        dot_file = ''
        classes_data = []
        try:
            paths = self.json_extract('paths')
            dot_file = paths['dot_file']
        except(KeyError):
            self.error += " the dot file doesn't exist in the config file"
            return
        except(TypeError):
            self.error += "there is an issue with the config file"
            self.error += "the paths segment cannot be found"
            return
        ##
        try:  # using regex to read .dot file
            with open(dot_file) as d:
                from re import findall
                from re import split
                for x in d:
                    splited = split("\|", x)  # [0] ends with class name,
                    # [1] has attributes separated by \\l
                    # [2] has functions separated by \\l
                    if(splited.__len__() > 2):
                        class_name = findall(r'\w*$', splited[0])[0]
                        attributes = findall('(.*?)\\\\l', splited[1])
                        methods = findall('(.*?)\\\\l', splited[2])
                        temp_list = []
                        temp_list.append(class_name)
                        temp_list.append(attributes)
                        temp_list.append(methods)
                        classes_data.append(temp_list)
                        (
                            {'name': class_name, 'atts': attributes,
                             'defs': methods})
        except(FileNotFoundError):
            print("this file does not exist")
            return

        command = self.json_extract('db_commands')
        table_exists = False
        try:
            assert command['delete_table'] == "DROP TABLE IF EXISTS "
            self.connection.execute(
                command['delete_table'] + command['table_name'])
            table_exists = False
        except(KeyError):
            print(
                'the config file has an error at "db_commands"["delete_table"] ')
            print('or [table_name]')
        except(AssertionError):
            print("delete command has been changed, " +
                  command['delete_table'] + " should be  DROP TABLE IF EXISTS ")
        try:
            self.connection.execute(command['create_table'])
            table_exists = True
        except(KeyError):
            print(
                'the config file has an error at "db_commands"["create_table"]')
        except(sqlite3.OperationalError):
            print('this table already exists, try deleting the table')
            print('due to an inconsistency in the config file')

        if(table_exists):
            self.add_data(classes_data)

    def add_data(self, classes_data):
        '''
        >>> add_data()
        Traceback (most recent call last):
        File "%\\doctest.py", line 1329, in __run
            compileflags, 1), test.globs)
        File "<doctest __main__.add_data[0]>", line 1, in <module>
            add_data()
        TypeError: add_data() missing 1 required positional argument: \
    'classes_data'
        '''

        command = self.json_extract()
        for obj in classes_data:
            att_str = []
            # first, get data from dot file
            for section in obj:
                if(type(section) != str):
                    attribute_list = ""
                    for individual_attribute in section:
                        attribute_list += individual_attribute + " "
                    att_str.append(attribute_list)
                else:
                    att_str.append(section.__str__())
            # then, add to database
            if(att_str.__len__() == 3):
                inputcommand = command['insert'] + command['table_name'] + \
                    'Values(" ' + att_str[0] + '","' + \
                    att_str[1] + '"," ' + att_str[2] + '"); '
                self.connection.execute(inputcommand)

    # extract data back from the database.

    def select_from_sql(self, ):
        try:
            cursor = self.connection.cursor()
            command = self.json_extract()
            cursor.execute(command['select'] + command['table_name'])
            result = cursor.fetchall()
        except:
            print("there is an error selecting from the database")
            result = []
        return result


"""
cli is the main user interface
to-do: Make cmd robust for when users enter unknown codes
validate data: checking is source file is python or is classes are correct
"""


class CommandLineInterface(Cmd):

    prompt = '>>>'
    file = None

    def __init__(self, controller):
        Cmd.__init__(self)
        self.name = "unknown"
        self.runner = controller

    def default(self, arg):
        print(arg)
        print(' is an incorrect command. Type ? or help to see command list')

    def do_introduce(self, unknown_name):
        """
        Syntax: introduce me
                Enter your name.
        then follow the prompt
        """
        if unknown_name == 'me':
            try:
                print('Welcome')
                if unknown_name:
                    unknown_name = (input("Please enter you name: "))
                    print('Hello ' + unknown_name)
                else:
                    print('Hello ' + self.name)
            except ValueError as e:
                print(f'The exception is: {e}')
            except KeyError as e:
                print(f'{e}: Not a command')
            finally:
                print('Type help or ? to see more available commands.')
        else:
            message = "Incorrect syntax. Type: [Introduce me]"
            print(message)

    def do_pickle(self, arg):
        """
        pickle a python file
        Syntax: pickle [file name]
                Enter the to_be name of the pickled file
        """
        try:
            from pickling import Pickling
            Pickling(arg, input("Please enter the name of file: ")).pickle_it()
        except TypeError as e:
            print(e)
        except():
            print("Error!!")

    def do_unpickle(self, arg):
        """
        load the pickled file of the classes
        Syntax: unpickle [pickled file_name]
        """
        try:
            from pickling import Pickling
            Pickling('output.pickle', arg).unpickle_it()
            print('The pickled file has been un-pickled')
        except FileNotFoundError as e:
            print(e)
        except():
            print("Error!!")

    def do_pickle_delete(self, arg):
        """
        Delete the pickled file
        Syntax:  pickle_delete [file name]
        :return:
        """
        try:
            from pickling import Pickling
            Pickling('exp', arg).delete_it()
        except FileNotFoundError as err:
            print(err)

    def do_create_dot_file(self, arg):
        """
        Create dot file using Pyreverse
        Syntax:
        """
        try:

            # name = input("Enter diagram image name: ")
            self.runner.make_dot_file()
        except ImportError as e:
            print(e)
        except():
            print("Error!!")

    def do_create_uml(self, arg):
        """
        Create uml diagram from dot file
        Syntax:
        """
        try:
            self.runner.make_uml_diagram()
        except():
            print("Error!!")

    def do_load(self, name):
        """
        load the DOT file of uml diagram
        Syntax: load
        """
        try:
            self.runner.run()

        except():
            print('Loading failed')

    def do_exit(self, arg):
        """
        Stop the program
        syntax: exit
        """
        print('Thank you for visiting.')
        return True

    def say(self, message):
        print(message)


# run everything on defaults


# run everything on defaults


class Runner:

    def __init__(self):
        x = 0
        self.command_line = CommandLineInterface(self)
        self.command_line.cmdloop()
        self.model = Model

    def make_dot_file(self):
        self.model = Dot_file()
        self.use_model()

    def make_uml_diagram(self):
        self.model = Uml()
        self.use_model()

    def run(self):
        self.model = Database_connector()
        self.use_model()

    def use_model(self):
        self.model.run()
        self.command_line.say(self.model.error)
