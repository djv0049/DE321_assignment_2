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


if __name__ == "__main__":
    args = split(json_extract('paths')['source_code'])
    try:  # reads, analyses, and creates .dot file from the destination file
        call(['pyreverse'] + args)
    except ValueError as e:  # if not, gives error message
        print('there was a problem converting the .py file with pyreverse', e)

    print("dot file created")
