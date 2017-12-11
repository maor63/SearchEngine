

from collections import defaultdict

from Indexer import Indexer
from Observable import Observable
from Parser import Parser
from ReadFile import ReadFile
from Stemmer import Stemmer
import time

class Master(Observable):
    def __init__(self, docs_path, postings_path):
        super().__init__()
        self.TermDictionary = {}
        self.DocsDictionary = {}
        self.file_reader = ReadFile()
        self.docs_path = docs_path
        self.parser = Parser("{0}/stop_words.txt".format(docs_path))
        self.stemmer = Stemmer()
        self.indexer = Indexer("{0}/".format(postings_path))

    def clean_indexing(self):
        self.indexer.clean_postings()

    def run_process(self, stemming=True, treshhold=2):
        start = time.time()
        corpus_path = "{0}/".format(self.docs_path)
        total_docs = self.file_reader.read_files(corpus_path, treshhold)
        docs_count = self.file_reader.count_docs(corpus_path)

        for next_docs in total_docs:
            batch_terms = []

            for doc in next_docs:
                terms_dict = self.parse_text(doc.text)
                if stemming:
                    terms_dict = self.stemmer.stem(terms_dict)
                batch_terms.append(terms_dict)
                self.indexer.index(terms_dict, doc)
            self.indexer.flush()
            progress = treshhold / docs_count * 100
            self.notify_observers(progress=progress, status='Indexing', done=False)
            print("batch ended")
        print("end")
        terms_postings = "merged_terms_postings.txt"
        docs_postings = 'merged_docs_postings.txt'
        if stemming:
            terms_postings = "stemed_" + terms_postings
            docs_postings = "stemed_" + docs_postings
        end = time.time()
        print("Read file time after parser: {0}".format(str((end - start)/60)+" min"))
        self.indexer.merge(terms_postings, docs_postings)
        end = time.time()
        print("Read file time after merge: {0}".format(str((end - start) / 60) + " min"))
        self.indexer.cache()
        end1 = time.time()
        print("Read file time after cache: {0}".format(str((end1 - start) / 60) + " min"))
        total_time = end - start
        self.indexer.print_messege(total_time)
        self.TermDictionary = self.indexer.TermDictionary
        self.DocsDictionary = self.indexer.DocsDictionary
        self.notify_observers(done=True)

    def combine_dicts(self, terms):
        new_term_dict = defaultdict(int)
        for term_dict in terms:
            for term in term_dict:
                new_term_dict[term] += term_dict[term]
        return dict(new_term_dict)

    def parse_text(self, text):
        return self.parser.parse(text)

    def get_term_dictionary(self):
        return self.TermDictionary

