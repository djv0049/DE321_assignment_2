"""
cli will have the cmd interface
to-do: Make cmd robust for when users enter unknown codes
validate data: checking is source file is python or is classes are correct
"""
from cmd import Cmd
from src_code import Hospital, Doctor, Nurse


class CommandLineInterface(Cmd):
    intro = 'Simple Cli for Assessment2. Please Start by typing [introduce me] and follow the prompt.\n'
    prompt = '>>>'
    file = None

    def __init__(self):
        Cmd.__init__(self)
        self.name = ""

    def do_name(self, unknown_name):
        try:
            if unknown_name:
                self.name = unknown_name
            print(self, unknown_name)
        except KeyError as e:
            print(f'{e}: Not a command')
        except ValueError as e:
            print(f'The exception is: {e}')

    def do_introduce(self, unknown_name):
        """
        Syntax: introduce [name]
        follow the prompt.h
        """
        if unknown_name == 'me':
            try:
                print('Welcome')
                if unknown_name:
                    unknown_name = (input("Please enter you name: "))
                    print('Hello ' + unknown_name)
                else:
                    print('Hello ' + self.name)
            except ValueError as e:
                print(f'The exception is: {e}')
            except KeyError as e:
                print(f'{e}: Not a command')
            finally:
                print('Type help or ? to see more available commands.')
        else:
            message = "Incorrect syntax. Type: [Introduce me]"
            print(message)

    def do_unpickle(self, line):
        """
        load the pickled file
        Syntax: unpickle
        """
        try:
            from pickling import un_pickle_it
            un_pickle_it()
        except SyntaxError as e:
            print(e)

    def do_load(self, line):
        """
        load the DOT diagram
        Syntax: load
        """
        try:
            f = open('classes.dot', 'r')
            print(f)
        except():
            print('Loading failed')

    def do_exit(self, line):
        """
        Stop the program
        syntax: exit
        """
        print('Thank you for visiting.')
        return True


if __name__ == '__main__':
    CommandLineInterface().cmdloop()
