from threading import Thread

import time

from Model import Model
from Observable import Observable
from Observer import Observer
from ReadFile import ReadFile
from Searcher import Searcher
from Summerizer import Summerizer


class Dictionary:
    def __init__(self, term_dict, docs_dict):
        self.term_dict = term_dict
        self.docs_dict = docs_dict


class Controller(Observer, Observable):
    def __init__(self):
        Observable.__init__(self)
        self.module = None
        self.term_dict = {}
        self.docs_dict = {}
        self.cache = {}
        self.query_results = []


    def start_indexing(self, doc_path, posting_path, stem):
        '''
        start the indexing process for creating Dictionary and Postings files 
        :param doc_path: path to the corpus
        :param posting_path: path where posting will be saved
        :param stem: True for activating stemming
        '''
        print("Stemming: {0}".format(stem))
        self.module = Model(doc_path, posting_path)
        self.module.set_observer(self)
        t = Thread(target=self.module.run_process, args=(stem, 100))
        t.start()

    def clean_postings(self):
        '''
        delete posting cache and dictionary files from postings path
        '''
        self.term_dict = {}
        self.docs_dict = {}
        self.cache = {}
        if self.module is not None:
            self.module.clean_indexing()

    def get_dictionary(self):
        '''
        :return: the Dictionary 
        '''
        d = Dictionary(self.term_dict, self.docs_dict)
        # return self.term_dict
        return d

    def get_cache(self):
        '''
        :return: the Cache
        '''
        return self.cache

    def get_results(self):
        '''
        :return: the Cache
        '''
        return self.query_results

    def set_cache(self, cache):
        '''
        set the cache
        '''
        self.cache = cache

    def set_dictionary(self, dictionary):
        '''
        set the dictionary
        '''
        self.docs_dict = dictionary.docs_dict
        self.term_dict = dictionary.term_dict

    def update(self, **kwargs):
        '''
        get updates from the Model 
        '''
        if "fail" in kwargs:
            self.notify_observers(**kwargs)
        elif kwargs['done']:
            self.term_dict = self.module.get_term_dictionary()
            self.docs_dict = self.module.get_doc_dictionary()
            self.cache = self.module.get_cache()
            self.notify_observers(status="Done!!!", done=True, progress=0, summary=kwargs['summary'])
        else:
            self.notify_observers(**kwargs)

    def search_query(self, query, query_num=0):
        start = time.time()
        self.searcher = Searcher("./test_data/stop_words.txt", self.get_dictionary().term_dict,
                                 self.get_dictionary().docs_dict, self.get_cache(), "./test_data/merged_terms_postings")
        self.query_results = {doc_id: query_num for doc_id in self.searcher.search_query(query)}
        totaltime = time.time() - start
        return self.query_results, totaltime

    def search_file_query(self, query_file):
        results = {}
        start = time.time()
        self.searcher = Searcher("./test_data/stop_words.txt", self.get_dictionary().term_dict,
                                 self.get_dictionary().docs_dict, self.get_cache(), "./test_data/merged_terms_postings")
        r = ReadFile()
        queries = r.read_query_file(query_file)
        query_num = 0
        for query in queries:
            query_num += 1
            self.query_results = {doc_id: query_num for doc_id in self.searcher.search_query(query)}
            results[query_num] = self.query_results
        totaltime = time.time() - start
        return results, totaltime


    # def save_query_results(self):
    #     f = open("results.txt", 'w')
    #     for doc_id in self.query_results:
    #         f.write("351   0  FR940104-0-00001  1   42.38   mt")


    # def summarize_document(self, doc_id, doc_path):
    #     s = Summerizer()
    #     r = ReadFile()
    #     docs = r.read_file_from_path(, doc_path
