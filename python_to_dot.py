from os.path import abspath, split
from os import system
from shlex import split
from json import load
from subprocess import call


def json_extract(component='db_commands'):
    with open('config.json') as config:
        result = load(config)
        result = result[component]
    return result

# find path to dot.exe file


args = split(json_extract('paths')['source_code'])
try:  # reads, analyses, and creates .dot file from the destination file
    call(['pyreverse'] + args)
except ValueError as e:  # if not, gives error message
    print('there was a problem converting the .py file with pyreverse', e)


# try
# execute the pyreverse on the source code with default arguments unless advised otherwise

# save the results as a .dot file


# -------- class for checking files exist (fileName and/or path)


# config should have the path to the dot.exe file.
# validate this

# config should also have a path to the source code .py file
# validate this


# -------- new class for creating uml from dot file

# check parameters. if none, then use default config files

# if parameters exist, check what they are and what they do.

# try
# execute the dot.exe file on the .dot

#


# to run this program, the user must have pip installed pylint to their env


# change terminals working directory to the one with the destination file in it

# the path to the bin folder with dot.exe for use later

# the destination file and any extras

# next step is to use something to draw the diagram from the .dot format.
# then expand and build features around, for extra functionality


# here i will try to read a file, extract the data within, and use it for the command line
print("dot created  ")
