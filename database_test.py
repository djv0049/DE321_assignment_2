# test_connect_to_database

import unittest


class testdata(unittest.TestCase):
    def test(self):
        # arrange
        from connect_to_database import Database_connector

        connection = Database_connector()

        self.assertEquals()

    def testSubclass(self):
        from create_uml import Uml
        from Imodel import Model
        c = issubclass(Uml, Model)
        print(c)


if __name__ == "__main__":
    t = testdata()
    t.testSubclass()
