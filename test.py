# import pylint
# from pylint import pyreverse
import json  # work with json
import subprocess  # calls the commandline
import shlex  # splits arguments into an array of arguments to be passed to terminal
import os  # gives access to terminal

# check parameters

# find path to config file
# Validate

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

# absolute path to the current file
script_path = os.path.abspath(__file__)

# gets the folder of the current file somehow
script_dir = os.path.split(script_path)[0]

# change terminals working directory to the one with the destination file in it
os.system('cd ' + script_dir)

# the path to the bin folder with dot.exe for use later
dot_file_path = (script_dir + "\\graphviz-2.38\\release\\bin\\dot.exe")

# the destination file and any extras
args = shlex.split('src_code.py')
try:  # reads, analyses, and creates .dot file from the destination file

    subprocess.call(['pyreverse'] + args)
except ValueError as e:  # if not, gives error message
    print('there was a problem converting the .py file with pyreverse', e)

# next step is to use something to draw the diagram from the .dot format.
# then expand and build features around, for extra functionality
args = shlex.split('classes.dot -Tpng -omy_classes.png')
subprocess.call([dot_file_path] + args)

print("done")

print("start phase 2")

# here i will try to read a file, extract the data within, and use it for the command line
with open('config.json') as config:
    data = json.load(config)
print(data["paths"]["source_code"])
