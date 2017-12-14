import os
from collections import defaultdict

import sys

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
        self.Cache = {}
        self.file_reader = ReadFile()
        self.docs_path = docs_path
        self.parser = Parser("{0}/stop_words.txt".format(docs_path))
        self.stemmer = Stemmer()
        self.posting_path = "{0}/".format(postings_path)
        self.indexer = Indexer(self.posting_path)

    def clean_indexing(self):
        self.indexer.clean_postings()

    def run_process(self, stemming=True, threshold=5):
        start = time.time()
        self.create_temp_postings(stemming, threshold)
        terms_postings = "merged_terms_postings.p"
        docs_postings = 'merged_docs_postings.p'
        if stemming:
            terms_postings = "stemed_" + terms_postings
            docs_postings = "stemed_" + docs_postings
        end = time.time()
        print("Read file time after indexing: {0}".format(str((end - start) / 60) + " min"))
        self.notify_observers(progress=50, status='Merging posting files', done=False)
        self.TermDictionary, self.DocsDictionary = self.indexer.merge_postings(terms_postings, docs_postings)

        end = time.time()
        print("Read file time after merge: {0}".format(str((end - start) / 60) + " min"))

        self.notify_observers(progress=50, status='Creating Cache', done=False)
        self.Cache = self.indexer.create_cache(10000)
        end1 = time.time()
        print("Read file time after cache: {0}".format(str((end1 - start) / 60) + " min"))
        total_time = end - start
        summary = {'term_indexed': len(self.TermDictionary), 'doc_indexed': len(self.DocsDictionary),
                   'total_time': round(total_time), 'cache_size': sys.getsizeof(self.Cache),
                   'terms_size': os.path.getsize(self.posting_path + terms_postings),
                   'docs_size': os.path.getsize(self.posting_path + docs_postings)}
        self.notify_observers(done=True, summary=summary)

    def create_temp_postings(self, stemming, threshold):
        corpus_path = "{0}/".format(self.docs_path)
        total_docs = self.file_reader.read_files(corpus_path, threshold)
        docs_count = self.file_reader.count_docs(corpus_path)
        for next_docs in total_docs:
            self.index_docs(next_docs, stemming)
            self.indexer.flush()
            progress = threshold / docs_count * 100
            self.notify_observers(progress=progress, status='Indexing', done=False)

    def index_docs(self, next_docs, stemming):
        for doc in next_docs:
            terms_dict = self.parse_text(doc.text)
            if stemming:
                terms_dict = self.stemmer.stem(terms_dict)
            self.indexer.index(terms_dict, doc)

    def parse_text(self, text):
        return self.parser.parse(text)

    def get_term_dictionary(self):
        return self.TermDictionary

    def get_cache(self):
        return self.Cache
