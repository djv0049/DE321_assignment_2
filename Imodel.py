# phython pure abstract superclass / interface for runer objects

from abc import ABC, abstractmethod


class Model(ABC):

    def __init__(self):
        self.error = ""

    def run(self):
        pass
