# run everything on defaults

from subprocess import call
from shlex import split


class Runner:
    def make_dot_file(self):
        call(split('python python_to_dot.py'))

    def make_uml_diagram(self):
        call(split('python create_uml.py'))

    def run(self):
        call(split('python connect_to_database.py'))
