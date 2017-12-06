from collections import defaultdict
from sortedcollections import SortedDict


class Indexer:
    def __init__(self, path=""):
        self.docs_posting = []
        self.terms_posting = []
        self.term_to_doc_id = SortedDict()
        self.path = path
        self._index = 1

    def index(self, terms_dict, doc):
        if len(terms_dict) == 0:
            return
        most_frequent = str(max(terms_dict, key=terms_dict.get))
        doc_row = "{0}#{1}#{2}\n".format(doc.id, most_frequent, str(len(doc.text)))
        self.docs_posting.append(doc_row)

        for term in terms_dict:
            if term not in self.term_to_doc_id:
                self.term_to_doc_id[term] = {}
            self.term_to_doc_id[term][doc.id] = terms_dict[term]

    def flush(self):
        for term in self.term_to_doc_id:
            term_row = term + "#" + str(len(self.term_to_doc_id[term]))
            for doc in self.term_to_doc_id[term]:
                term_row += "#{0}:{1}".format(doc, self.term_to_doc_id[term][doc])
            term_row += '\n'
            self.terms_posting.append(term_row)

        f_terms = open("{0}{1}_terms".format(self.path, str(self._index)), 'w')
        f_terms.writelines(self.terms_posting)
        # f_terms.flush()
        f_terms.close()

        f_docs = open("{0}{1}_docs".format(self.path, str(self._index)), 'w')
        f_docs.writelines(self.docs_posting)
        # f_docs.flush()
        f_docs.close()

        self.docs_posting = []
        self.terms_posting = []
        self.term_to_doc_id = SortedDict()
        self._index += 1
