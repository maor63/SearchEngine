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

    def start_indexing(self, doc_path, posting_path, stem):
        executor = ThreadPoolExecutor(max_workers=5)
        print("Stemming: {0}".format(stem))
        self.module = Master(doc_path, posting_path)
        self.module.set_observer(self)
        t = Thread(target=self.module.run_process, args=(stem, 5))
        t.start()
        # self.module.run_process(stem)
        # executor.submit(self.module.run_process, stem)
        # self.term_dict = future_term_dict.result()
        # self.docs_dict = future_docs_dict.result()

    def clean_postings(self):
        self.term_dict = {}
        self.docs_dict = {}
        if self.module is not None:
            self.module.clean_indexing()

    def get_dictionary(self):
        return self.term_dict

    def update(self, **kwargs):
        if kwargs['done']:
            self.term_dict = self.module.get_term_dictionary()
            self.notify_observers(status="Done!!!", done=True, progress=0)
        else:
            self.notify_observers(**kwargs)
