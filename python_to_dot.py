from os.path import abspath, split
from os import system
from shlex import split
from json import load
from subprocess import call
from Imodel import Model


class Dot_file(Model):

    def __init__(self):
        super().__init__()
        self.error = ""

    def run(self):
        args = split(self.json_extract('paths')[
                     'source_code'] + self.json_extract('misc')['py_to_dot_args'])
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
        except FileNotFoundError as e:
            return('check the file path in the config file. ' + args + ' \nFile not found')
