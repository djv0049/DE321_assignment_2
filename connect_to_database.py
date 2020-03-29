from subprocess import call
import json
import sqlite3  # database interactions
import doctest  # not doing much yet
from os import path
from shlex import split
# get path to config file

# read config file


# intake string of database name
# if no name, set database name to be json_extract('db_commands'['db'])
# create database

def connect(db=None):
    '''
    >>> type(connect())
    <class 'sqlite3.Connection'>


    '''
    #  assert(db is None)
    if (db is None):
        js = json_extract()
        db = js['db']
    try:
        connection = sqlite3.connect(db)
    except():
        print("error at creating database")

    return connection


def json_extract(component='db_commands'):
    '''
    make sure that the method gets a dictionary from json by default
    >>> type(json_extract())
    <class 'dict'>

    >>> json_extract('json_test')
    {'item_one': 'one', 'item_two': 'two'}

    '''

    with open('config.json') as config:
        result = json.load(config)
        result = result[component]
    return result


# uses regex to read a dot file, and creates tables from data
def make_tables(connection):
    dot_file = ''
    classes_data = []

    try:
        paths = json_extract('paths')
        dot_file = paths['dot_file']
    except(KeyError):
        print(" the dot file doesn't exist in the config file")
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
    command = json_extract('db_commands')
    table_exists = False
    try:
        connetion.execute(command['delete_table'] + command['table_name'])
        table_exists = False
    except(KeyError):
        print('the config file has an error at "db_commands"["delete_table"]')
    try:
        connection.execute(command['create_table'])
        table_exists = True
    except(KeyError):
        print('the config file has an error at "db_commands"["create_table"]')
    except(sqlite3.OperationalError):
        print('this table already exists, try deleting the table')
        print('due to an inconsistency in the config file')

    if(table_exists):
        add_data(classes_data)


def add_data(classes_data):
    command = json_extract()
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
            connetion.execute(inputcommand)


# extract data back from the database.

def select_from_sql(connection):
    try:
        cursor = connection.cursor()
        command = json_extract()
        cursor.execute(command['select'] + command['table_name'])
        result = cursor.fetchall()
    except:
        print("there is an error selecting from the database")
        result = []
    return result


if __name__ == "__main__":
    doctest.testmod()
    connetion = connect()
    make_tables(connetion)
    data = select_from_sql(connetion)
    if(data.__len__() > 1):
        print("the data in the database is :\n")
        print(data)
        print('\ndatabase complete')
    else:
        print(data)
        print("the database is empty")
