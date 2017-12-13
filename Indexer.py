import linecache
import os
from collections import Counter
from tkinter import *
import codecs
from tkinter import messagebox
from sortedcollections import SortedDict


class Indexer:
    def __init__(self, path=""):
        self.TermDictionary = {}
        self.DocsDictionary = {}
        self.Cache = {}
        self.terms_output_file = ''
        self.docs_output_file = ''

        self.docs_posting = []
        self.terms_posting = []
        self.term_to_doc_id = SortedDict()
        self.path = path
        self._index = 0
        self.message = "\n"

    def index(self, terms_dict, doc):
        if len(terms_dict) == 0:
            return
        most_frequent = str(max(terms_dict, key=terms_dict.get))
        doc_row = "{0}#{1}#{2}#{3}\n".format(doc.id, most_frequent, terms_dict[most_frequent], str(len(doc.text)))
        self.docs_posting.append(doc_row)

        for term in terms_dict:
            if term not in self.term_to_doc_id:
                self.term_to_doc_id[term] = {}
            self.term_to_doc_id[term][doc.id] = terms_dict[term]

    def clean_postings(self):
        postings_files = list(filter(lambda x: x.endswith('.p'), os.listdir(self.path)))
        for f in postings_files:
            os.remove(self.path + f)

    def flush(self):
        for term in self.term_to_doc_id:
            term_row = term + "#" + str(len(self.term_to_doc_id[term])) + "#"
            for doc in self.term_to_doc_id[term]:
                term_row += "{0}:{1}*".format(doc, self.term_to_doc_id[term][doc])
            term_row += '\n'
            self.terms_posting.append(term_row)

        if len(self.terms_posting) > 0:
            f_terms = codecs.open("{0}{1}_terms".format(self.path, str(self._index)), 'w', 'utf-8')
            f_terms.writelines(self.terms_posting)
            f_terms.close()

        if len(self.docs_posting) > 0:
            f_docs = codecs.open("{0}{1}_docs".format(self.path, str(self._index)), 'w', 'utf-8')
            f_docs.writelines(self.docs_posting)
            f_docs.close()

        self.docs_posting = []
        self.terms_posting = []
        self.term_to_doc_id = SortedDict()
        self._index += 1

    def merge(self, terms_output_file, docs_output_file):
        self.terms_output_file = terms_output_file
        self.docs_output_file = docs_output_file
        files_names = list(filter(lambda f: f.endswith("terms"), os.listdir(self.path)))
        files = list(map(lambda f: open(self.path + f), files_names))
        self.TermDictionary = self.merge_files(terms_output_file, files, self.merge_term_line,
                                               self.get_term_data_for_dictionary)

        files_names = list(filter(lambda f: f.endswith("docs"), os.listdir(self.path)))
        files = list(map(lambda f: open(self.path + f), files_names))
        self.DocsDictionary = self.merge_files(docs_output_file, files, self.merdge_doc_line,
                                               self.get_doc_data_for_dictionary)

    def merge_files(self, output_file, input_files, merge_line_fn, get_data_for_dict_fn):
        dictionary = {}
        file_row = 1
        output_file = open(self.path + output_file, 'w')
        while len(input_files) > 0:
            sorted_lines = SortedDict()
            files_to_delete = set()
            lines_limit = 3
            for i in range(lines_limit):
                remove = False
                for file in input_files:
                    line = file.readline()
                    if line == '':
                        file.close()
                        files_to_delete.add(file.name)
                        remove = True
                        continue
                    merge_line_fn(line, sorted_lines)
                if remove:
                    break
            if len(files_to_delete) > 0:
                [os.remove(file) for file in files_to_delete]
            for term in sorted_lines:
                output_file.write(sorted_lines[term])
                term_data = get_data_for_dict_fn(file_row, sorted_lines, term)
                dictionary[term] = term_data
                file_row += 1
            output_file.flush()
            input_files = list(filter(lambda x: x.name not in files_to_delete, input_files))
        output_file.close()
        return dictionary

    def get_doc_data_for_dictionary(self, file_row, sorted_lines, doc_id):
        doc_id, most_frequent_term, term_count, doc_size = sorted_lines[doc_id].split('#')
        doc_data = {'doc_id': doc_id, 'row': file_row}
        return doc_data

    def get_term_data_for_dictionary(self, file_row, sorted_lines, term):
        term, df, docs = sorted_lines[term].split('#')
        sum_tf = sum(map(lambda x: int(x.split(':')[1]), docs.split('*')[:-1]))
        term_data = {'row': file_row, 'sum_tf': sum_tf, 'df': df}
        return term_data

    def merge_term_line(self, line, sorted_lines):
        term, frec, doc_list = line.split('#')
        if term not in sorted_lines:
            sorted_lines[term] = line
        else:
            term2, frec2, doc_list2 = sorted_lines[term].split('#')
            sorted_lines[term] = '#'.join([term, str(int(frec) + int(frec2)), doc_list.rstrip() + doc_list2])

    def merdge_doc_line(self, line, sorted_lines):
        doc_data = line.split('#')
        sorted_lines[doc_data[0]] = line

    def cache(self, limit):
        term_frequency = Counter()
        for term in self.TermDictionary:
            term_frequency[term] = self.TermDictionary[term]['df']

        most_common_terms = term_frequency.most_common(int(limit * 0.8))
        docs_frequency = Counter()
        for term, frec in most_common_terms:
            row = self.TermDictionary[term]['row']
            term_data = linecache.getline(self.path + self.terms_output_file, row)
            self.Cache[term] = term_data
            docs_with_term = [doc.split(':')[0] for doc in term_data.split('#')[2].split('*')]
            docs_frequency.update(docs_with_term[:-1])
            self.TermDictionary[term]['row'] = -1

        most_common_docs = docs_frequency.most_common(int(limit * 0.2))
        for doc, frec in most_common_docs:
            row = self.DocsDictionary[doc]['row']
            doc_data = linecache.getline(self.path + self.docs_output_file, row)
            self.Cache[doc] = doc_data
            self.DocsDictionary[doc]['row'] = -1
        return self.Cache


