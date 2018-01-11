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
        t = Thread(target=self.module.run_process, args=(stem, 200))
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

    def search_query(self, doc_path, posting_path, query, query_num=0):
        start = time.time()
        d = self.get_dictionary()
        self.searcher = Searcher(doc_path + "/stop_words.txt", d.term_dict,
                                 d.docs_dict, self.get_cache(), posting_path + "/merged_terms_postings")
        self.query_results = {query_num: self.searcher.search_query(query)}
        totaltime = time.time() - start
        return self.query_results, totaltime

    def search_file_query(self, doc_path, posting_path, query_file):
        results = {}
        start = time.time()
        d = self.get_dictionary()
        self.searcher = Searcher(doc_path + "/stop_words.txt", d.term_dict,
                                 d.docs_dict, self.get_cache(), posting_path + "/merged_terms_postings")
        r = ReadFile()
        queries = r.read_query_file(query_file)
        query_num = 0
        for query in queries:
            query_num = queries[query]
            results.update({query_num: self.searcher.search_query(query)})
        totaltime = time.time() - start
        self.query_results = results
        return results, totaltime

    def save_query_results(self, file_result):
        # f = open("results.txt", 'w')
        for query_id in self.query_results:
            for doc_id in self.query_results[query_id]:
                file_result.write("{0}   0  {1}  1   42.38   mt\n".format(query_id, doc_id))

    def summarize_document(self, doc_id, docs_path):
        summerizer = Summerizer(docs_path + "/stop_words.txt")
        file_name = self.docs_dict[doc_id]['file_name'].strip()
        r = ReadFile()
        t = "{0}/corpus/".format(docs_path)
        docs = r.read_file_from_path(t, file_name)
        doc = list(filter(lambda d: d.id == doc_id, docs))[0]
        res = summerizer.get_importent_sentences(doc, 5)
        return res
