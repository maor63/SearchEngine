from Parser import Parser


class Searcher:
    def __init__(self):
        self.parser = Parser()

    def search_query(self, query):
        self.parser.parse(query)
        