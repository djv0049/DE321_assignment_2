"""
cli is the main user interface
to-do: Make cmd robust for when users enter unknown codes
validate data: checking is source file is python or is classes are correct
"""
from cmd import Cmd


class CommandLineInterface(Cmd):

    prompt = '>>>'
    file = None

    def __init__(self, controller):
        Cmd.__init__(self)
        self.name = "unknown"
        self.runner = controller
        self.cmdloop()

    def default(self, arg):
        self.say(arg)
        self.say(' is an incorrect command. Type ? or help to see command list')

    def do_introduce(self, unknown_name):
        """
        Syntax: introduce me
                Enter your name.
        then follow the prompt
        """
        if unknown_name == 'me':
            try:
                self.say('Welcome')
                if unknown_name:
                    unknown_name = (input("Please enter you name: "))
                    self.say('Hello ' + unknown_name)
                else:
                    self.say('Hello ' + self.name)
            except ValueError as e:
                self.say(f'The exception is: {e}')
            except KeyError as e:
                self.say(f'{e}: Not a command')
            finally:
                self.say('Type help or ? to see more available commands.')
        else:
            message = "Incorrect syntax. Type: [Introduce me]"
            self.say(message)

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
            self.say(e)
        except():
            self.say("Error!!")

    def do_unpickle(self, arg):
        """
        load the pickled file of the classes
        Syntax: unpickle [pickled file_name]
        """
        try:
            from pickling import Pickling
            Pickling('output.pickle', arg).unpickle_it()
            self.say('The pickled file has been un-pickled')
        except FileNotFoundError as e:
            self.say(e)
        except():
            self.say("Error!!")

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
            self.say(err)

    def do_create_dot_file(self, arg):
        """
        Create dot file using Pyreverse
        Syntax:
        """
        try:

            # name = input("Enter diagram image name: ")
            self.runner.make_dot_file()
        except ImportError as e:
            self.say(e)
        except():
            self.say("Error!!")

    def do_create_uml(self, arg):
        """
        Create uml diagram from dot file
        Syntax:
        """
        try:
            self.runner.make_uml_diagram()
        except():
            self.say("Error!!")

    def do_load(self, name):
        """
        load the DOT file of uml diagram
        Syntax: load
        """
        try:
            self.runner.run()

        except():
            self.say('Loading failed')

    def do_exit(self, arg):
        """
        Stop the program
        syntax: exit
        """
        self.say('Thank you for visiting.')
        return True

    def say(self, message):
        print(message)
