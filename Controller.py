from Master import Master


class Controller:
    def __init__(self):
        self.module = None

    def start_indexing(self, doc_path, posting_path, stem):
        print("Stemming: {0}".format(stem))
        self.module = Master(doc_path, posting_path)
        terms_dict, docs_dict = self.module.run_process(stemming=stem)
        pass

    def clean_postings(self):
        if self.module is not None:
            self.module.clean_indexing()

