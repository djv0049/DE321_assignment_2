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
    if db is None:
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
        print("this object doesn't exist in the config file")
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
                    attributes = findall(r'(.*?)\\\\l', splited[1])
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
        print('this table already exists, try deleting the table. this will be')
        print('due to an inconsistency in the config file')

    if(table_exists):
        add_data(classes_data)


def add_data(classes_data):
    command = json_extract()
    for obj in classes_data:
        att_str = []
        for section in obj:
            if(type(section) != str):
                attribute_list = ""
                for individual_attribute in section:
                    attribute_list += individual_attribute + " "
                att_str.append(attribute_list)
            else:
                att_str.append(section.__str__())
        print(att_str)
        # double checking that there are 3 values in the object
        if(att_str.__len__() == 3):
            inputcommand = command['insert'] + command['table_name'] + \
                'Values(" ' + att_str[0] + '","' + \
                att_str[1] + '"," ' + att_str[2] + '"); '
            print(inputcommand)
            connetion.execute(inputcommand)


# extract data back from the database.

def select_from_sql(connection):
    try:
        cursor = connection.cursor()
        command = json_extract()
        cursor.execute(command['select'] + command['table_name'])
        print(cursor.fetchall())
    except:
        print("last error")
    print('done')
    # somehow format the data from database and .dot file into a medium format

    # somehow validate the data extracted from the database
    # is the same as the data in the classes.dot file

    # tell the cmd that the task is done
    # hard coded values to be fixed with variables and assert/try-catch
    # statements to make sure value is correct


if __name__ == "__main__":
    doctest.testmod()
    connetion = connect()
    make_tables(connetion)
    select_from_sql(connetion)
    print('database done')
