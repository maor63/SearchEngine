from concurrent.futures import ThreadPoolExecutor

from collections import defaultdict

from Indexer import Indexer
from Parser import Parser
from ReadFile import ReadFile
from Stemmer import Stemmer


class Master:
    def __init__(self):
        self.file_reader = ReadFile()
        self.parser = Parser("stop_words.txt")
        self.stemmer = Stemmer()
        self.indexer = Indexer("./postings/")

    def run_process(self):
        to_stem = False
        executor = ThreadPoolExecutor(max_workers=7)
        total_docs = self.file_reader.read_files("./corpus1/", 1000)
        threads = []
        stem = True
        for next_docs in total_docs:
            batch_terms = []

            for doc in next_docs:
                terms_dict = self.parse_text(doc.text)
                if to_stem:
                    terms_dict = self.stemmer.stem(terms_dict)
                batch_terms.append(terms_dict)
                self.indexer.index(terms_dict, doc)
            self.indexer.flush()
            print("batch ended")
        print("end")
        self.indexer.merge()
        self.indexer.cache()

    def combine_dicts(self, terms):
        new_term_dict = defaultdict(int)
        for term_dict in terms:
            for term in term_dict:
                new_term_dict[term] += term_dict[term]
        return dict(new_term_dict)

    def parse_text(self, text):
        return self.parser.parse(text)

