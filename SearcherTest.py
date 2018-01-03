import pickle
import unittest

from Controller import Controller
from Searcher import Searcher


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.searcher = Searcher("")
        self.c = Controller()
        self.c.set_dictionary(pickle.load("C:/Users/אלון/Desktop/dic.dic"))
        self.c.set_cache(pickle.load("C:/Users/אלון/Desktop/cch.chh"))

    def test(self):
        self.searcher.search_query("cent")


