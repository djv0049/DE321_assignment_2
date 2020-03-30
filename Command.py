"""
cli is the main user interface
to-do: Make cmd robust for when users enter unknown codes
validate data: checking is source file is python or is classes are correct
"""
from cmd import Cmd


class CommandLineInterface(Cmd):

    prompt = '>>>'
    file = None

    def __init__(self):
        Cmd.__init__(self)
        self.name = "unknown"

    def default(self, arg):
        print(arg)
        print(' is an incorrect command. Type ? or help to see command list')

    def do_introduce(self, unknown_name):
        """
        Syntax: introduce me
                Enter your name.
        then follow the prompt
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

    def do_pickle(self, arg):
        """
        pickle a python file
        Syntax: pickle [file name]
                Enter the to_be name of the pickled file
        """
        try:
            from pickling import Pickling
            Pickling(arg, input("Please enter the name of file: ")).pickle_it()
        except TypeError as e:
            print(e)
        except():
            print("Error!!")

    def do_unpickle(self, arg):
        """
        load the pickled file of the classes
        Syntax: unpickle [pickled file_name]
        """
        try:
            from pickling import Pickling
            Pickling('output.pickle', arg).unpickle_it()
            print('The pickled file has been un-pickled')
        except FileNotFoundError as e:
            print(e)
        except():
            print("Error!!")

    def do_pickle_delete(self, arg):
        """
        Delete the pickled file
        Syntax:  pickle_delete [file name]
        :return:
        """
        try:
            from pickling import Pickling
            Pickling('exp', arg).delete_it()
        except FileNotFoundError as err:
            print(err)

    def do_create_dot_file(self, arg):
        """
        Create dot file using Pyreverse
        Syntax:
        """
        try:
            from runner import Runner
            # name = input("Enter diagram image name: ")
            Runner().make_dot_file()
        except ImportError as e:
            print(e)
        except():
            print("Error!!")

    def do_create_uml(self, arg):
        """
        Create uml diagram from dot file
        Syntax:
        """
        try:
            from runner import Runner
            Runner().make_uml_diagram()
        except ImportError as e:
            print(e)
        except():
            print("Error!!")

    def do_load(self, name):
        """
        load the DOT file of uml diagram
        Syntax: load
        """
        try:
            from runner import Runner
            Runner().run()
        except ImportError as e:
            print(e)
        except():
            print('Loading failed')

    def do_exit(self, arg):
        """
        Stop the program
        syntax: exit
        """
        print('Thank you for visiting.')
        return True


if __name__ == '__main__':
    CommandLineInterface().cmdloop()
