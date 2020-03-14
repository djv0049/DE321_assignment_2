import pylint
from pylint import pyreverse
import subprocess
import shlex

import os  # gives access to terminal
script_path = os.path.abspath(__file__)  # absolute path to the current file
# gets the folder of the current file somehow
script_dir = os.path.split(script_path)[0]
# change terminals working directory to the one with the destination file in it
os.system('cd ' + script_dir)
# reads, analyses, and creates .dot file from the destination file
args = shlex.split('src_code.py')  # the destination file
subprocess.call(['pyreverse'] + args)
# next step is to use graphviz to draw the diagram from the .dot format. then expand

# Run(args)
#
