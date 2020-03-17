import pylint
from pylint import pyreverse
import subprocess
import shlex
import tkinter
#import graphviz
import os  # gives access to terminal


# the path to the bin folder with dot.exe
# dot_file_path = ("C:\\Users\\djv0049\\OneDrive - Ara Institute of Canterbury\\Ara\\Semester 4\\AdvancedProgramming\\Assesment_2\\graphviz-2.38\\release\\bin\\dot.exe")
dot_file_path = (
    "C:\\Users\\djv0049\\OneDrive - Ara Institute of Canterbury\\Ara\\Semester 4\\AdvancedProgramming\\Assesment_2\\graphviz-2.38\\release\\bin\\dot.exe")
script_path = os.path.abspath(__file__)  # absolute path to the current file
# gets the folder of the current file somehow
script_dir = os.path.split(script_path)[0]
# change terminals working directory to the one with the destination file in it
os.system('cd ' + script_dir)
# the destination file and any extras
args = shlex.split('src_code.py')
try:  # reads, analyses, and creates .dot file from the destination file
    subprocess.call(['pyreverse'] + args)
except():  # if not, gives error message
    print('there was a problem converting the .py file with pyreverse')
# next step is to use something to draw the diagram from the .dot format. then expand

args = shlex.split('classes.dot -Tpng -omy_classes.png')
subprocess.call([dot_file_path] + args)

print("done")

# Run(args)
#
