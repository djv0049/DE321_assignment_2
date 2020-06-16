# run everything on defaults

from subprocess import call
from shlex import split
from connect_to_database import Database_connector
from Command import CommandLineInterface
from python_to_dot import Dot_file
from create_uml import Uml
from Imodel import Model


class Runner:

    def __init__(self):
        x = 0
        self.views = set()
        self.addView(CommandLineInterface(self))

    def addView(self, model):
        self.views.add(model)

    def showMessage(self, message):
        for view in self.views:
            view.say(message)

    def make_dot_file(self):
        model = Dot_file()
        self.use_model(model)

    def make_uml_diagram(self):
        model = Uml()
        self.use_model(model)

    def run(self):
        model = Database_connector()
        self.use_model(model)

    def use_model(self, model):
        model.run()
        self.showMessage(model.error)
