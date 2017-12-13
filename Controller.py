from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from Master import Master
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
        print("Stemming: {0}".format(stem))
        self.module = Master(doc_path, posting_path)
        self.module.set_observer(self)
        t = Thread(target=self.module.run_process, args=(stem, 5))
        t.start()

    def clean_postings(self):
        self.term_dict = {}
        self.docs_dict = {}
        self.cache = {}
        if self.module is not None:
            self.module.clean_indexing()

    def get_dictionary(self):
        return self.term_dict

    def get_cache(self):
        return self.cache

    def update(self, **kwargs):
        if kwargs['done']:
            self.term_dict = self.module.get_term_dictionary()
            self.cache = self.module.get_cache()
            self.notify_observers(status="Done!!!", done=True, progress=0, summary=kwargs['summary'])
        else:
            self.notify_observers(**kwargs)
