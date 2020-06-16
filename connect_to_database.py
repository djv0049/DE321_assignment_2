from subprocess import call
import json
import sqlite3  # database interactions
import doctest  # not doing much yet
from os import path
from shlex import split
from Imodel import Model
# get path to config file

# read config file


class Database_connector(Model):
    # intake string of database name
    # if no name, set database name to be json_extract('db_commands'['db'])
    # create database

    def __init__(self):
        super().__init__()
        doctest.testmod()

    def run(self):
        self.connection = self.connect()
        self.make_tables()
        data = self.select_from_sql()
        self.error = "the data in the database is :\n"
        self.error += str(data)

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
