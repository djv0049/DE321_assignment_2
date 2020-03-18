#import pylint
#from pylint import pyreverse
import subprocess
import shlex
import os  # gives access to terminal

### to run this program, the user must have pip installed pylint to their env

# split all this crap into methods

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
args += shlex.split()
try:  # reads, analyses, and creates .dot file from the destination file

    subprocess.call(['pyreverse'] + args)
except():  # if not, gives error message
    print('there was a problem converting the .py file with pyreverse')

# next step is to use something to draw the diagram from the .dot format.
# then expand and build features around, for extra functionality
args = shlex.split('classes.dot -Tpng -omy_classes.png')
subprocess.call([dot_file_path] + args)

print("done")

def getPythonSrc():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]