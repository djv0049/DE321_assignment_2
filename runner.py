# run everything on defaults

from subprocess import call
from shlex import split
call(split('python python_to_dot.py'))
call(split('python create_uml.py'))
call(split('python connect_to_database.py'))
