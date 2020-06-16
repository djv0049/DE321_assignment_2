
from pylint import pyreverse
import graphviz
from os.path import abspath, split as os_split
from os import system
from shlex import split
from json import load
from subprocess import call as sub_call
from sys import argv
from Imodel import Model


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
