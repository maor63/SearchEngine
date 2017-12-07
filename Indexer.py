import heapq
import linecache
from collections import defaultdict

import os
from sortedcollections import SortedDict


class Indexer:
    def __init__(self, path=""):
        self.docs_posting = []
        self.terms_posting = []
        self.term_to_doc_id = SortedDict()
        self.path = path
        self._index = 1
        f_docs = open("{0}docs".format(self.path), 'w')

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
            term_row = term + "#" + str(len(self.term_to_doc_id[term])) + "#"
            for doc in self.term_to_doc_id[term]:
                term_row += "{0}:{1}*".format(doc, self.term_to_doc_id[term][doc])
            term_row += '\n'
            self.terms_posting.append(term_row)

        f_terms = open("{0}{1}_terms".format(self.path, str(self._index)), 'w')
        f_terms.writelines(self.terms_posting)
        # f_terms.flush()
        f_terms.close()

        f_docs = open("{0}docs".format(self.path), 'a')
        f_docs.writelines(self.docs_posting)
        # f_docs.flush()
        f_docs.close()

        self.docs_posting = []
        self.terms_posting = []
        self.term_to_doc_id = SortedDict()
        self._index += 1

    def merge(self):
        file_terms = list((filter(lambda f: "terms" in f, os.listdir(self.path))))
        num = 1
        # file_terms.remove(file_terms[8])
        open(self.path + 'merged', 'w')
        while len(file_terms) > 1:
            file1 = file_terms[0]
            file2 = file_terms[1]
            self.mergefiles(open(self.path + file1), open(self.path + file2), 'merged', num)
            file_terms.remove(file1)
            file_terms.remove(file2)
            os.remove(self.path + file1)
            os.remove(self.path + file2)
            file_terms.append("merged" + str(num) + "_terms")
            num += 1
        os.remove(self.path + 'merged')

    def mergefiles(self, file1, file2, output, num):
        d = SortedDict()
        x = file1.readline()
        y = file2.readline()
        if y != '':
            term2, freq2, doc_list2 = y.split('#')
        while x != '':
            term1, freq1, doc_list1 = x.split('#')
            if term1 < term2:
                d[term1] = x
                x = file1.readline()
                if x == '':
                    break
                term1, freq1, doc_list1 = x.split('#')
            elif term2 < term1:
                d[term2] = y
                y = file2.readline()
                if y == '':
                    break
                term2, freq2, doc_list2 = y.split('#')
            else:
                freq = int(freq1) + int(freq2)
                doc_list = doc_list1.rstrip() + doc_list2
                d[term1] = '#'.join([term1, str(freq), doc_list])
                x = file1.readline()
                if x == '':
                    break
                term1, freq1, doc_list1 = x.split('#')
                y = file2.readline()
                if y == '':
                    break
                term2, freq2, doc_list2 = y.split('#')

        while y != '':
            d[term2] = y
            y = file2.readline()
            if y == '':
                break
            term2, freq2, doc_list2 = y.split('#')

        file1.close()
        file2.close()

        print("end")
        l = []
        for term in d:
            l.append(d[term])


        f_terms = open("{0}{1}{2}_terms".format(self.path, output, num), 'w')
        f_terms.writelines(l)
        # f_terms.flush()
        f_terms.close()

        self.docs_posting = []
        self.terms_posting = []
