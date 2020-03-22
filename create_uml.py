
from pylint import pyreverse
import graphviz
from os.path import abspath, split as os_split
from os import system
from shlex import split
from json import load
from subprocess import call as sub_call
from sys import argv


def json_extract(component='db_commands'):
    with open('config.json') as config:
        result = load(config)
        result = result[component]
    return result


def main():
    script_path = abspath(__file__)
    script_dir = os_split(script_path)[0]
    system('cd ' + script_dir)
    dot_file_path = (script_dir + "\\" + json_extract('paths')['dot.exe'])
    destination_file = json_extract('paths')['dot_file']
    print(argv.__len__())
    args = ""
    if argv.__len__() < 2:
        args = '-Tpng -omy_classes.png'
    else:
        for arg in argv[1:]:
            args += arg
            print(arg)
    ar = [dot_file_path]+[destination_file] + split(args)
    try:
        sub_call(ar)
        print('uml done')
    except(PermissionError):
        print("you don't Hve valid permissions to create this file")
    except(FileNotFoundError):
        print("cannof find file at " + ar)


if __name__ == "__main__":
    main()
