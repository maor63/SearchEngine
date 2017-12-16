from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from Model import Model
from Observable import Observable
from Observer import Observer


class Controller(Observer, Observable):
    def __init__(self):
        Observable.__init__(self)
        self.module = None
        self.term_dict = {}
        self.docs_dict = {}
        self.cache = {}

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
        t = Thread(target=self.module.run_process, args=(stem, 5))
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
        return self.term_dict

    def get_cache(self):
        '''
        :return: the Cache
        '''
        return self.cache

    def set_cache(self, cache):
        '''
        set the cache
        '''
        self.cache = cache

    def set_dictionary(self, dictionary):
        '''
        set the dictionary
        '''
        self.term_dict = dictionary

    def update(self, **kwargs):
        '''
        get updates from the Model 
        '''
        if kwargs['done']:
            self.term_dict = self.module.get_term_dictionary()
            self.cache = self.module.get_cache()
            self.notify_observers(status="Done!!!", done=True, progress=0, summary=kwargs['summary'])
        else:
            self.notify_observers(**kwargs)


