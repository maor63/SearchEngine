import os
from tkinter import *

from tkinter import messagebox
from sortedcollections import SortedDict


class Indexer:
    def __init__(self, path=""):
        self.TermDictionary = {}
        self.DocsDictionary = {}

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
        for f in os.listdir(self.path):
            os.remove(self.path + f)

    def flush(self):
        for term in self.term_to_doc_id:
            term_row = term + "#" + str(len(self.term_to_doc_id[term])) + "#"
            for doc in self.term_to_doc_id[term]:
                term_row += "{0}:{1}*".format(doc, self.term_to_doc_id[term][doc])
            term_row += '\n'
            self.terms_posting.append(term_row)

        if len(self.terms_posting) > 0:
            f_terms = open("{0}{1}_terms".format(self.path, str(self._index)), 'w')
            f_terms.writelines(self.terms_posting)
            f_terms.close()

        if len(self.docs_posting) > 0:
            f_docs = open("{0}{1}_docs".format(self.path, str(self._index)), 'w')
            f_docs.writelines(self.docs_posting)
            f_docs.close()

        self.docs_posting = []
        self.terms_posting = []
        self.term_to_doc_id = SortedDict()
        self._index += 1

    def merge(self, terms_output_file, docs_output_file):
        files_names = list(filter(lambda f: f.endswith("terms"), os.listdir(self.path)))
        files = list(map(lambda f: open(self.path + f), files_names))
        self.TermDictionary = self.merge_files(terms_output_file, files, self.merge_term_line, self.get_term_data_for_dictionary)

        files_names = list(filter(lambda f: f.endswith("docs"), os.listdir(self.path)))
        files = list(map(lambda f: open(self.path + f), files_names))
        self.DocsDictionary = self.merge_files(docs_output_file, files, self.merdge_doc_line, self.get_doc_data_for_dictionary)
        self.message = self.message + "The number of terms indexed: {0:,} terms\n\n" \
                                      "The number of Docs that were indexed: {1:,} Docs\n\n".format \
            (len(self.TermDictionary), len(self.DocsDictionary))

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

    def cache(self):
        f_cache = open("{0}cache".format(self.path), 'a')
        line = 0
        maxfrequency = []
        counter = 1
        dicfreqlines = {}
        file = open("{0}merged_terms_postings.txt".format(self.path), 'r')
        newfile = open(self.path + "new_merged_terms", 'a')
        x = file.readline()
        while (x != ''):
            term, freq, doc_list = x.split('#')
            dicfreqlines[line] = int(freq)
            line += 1
            x = file.readline()

        while (counter <= 100):
            maxfrequency.append(max(dicfreqlines, key=dicfreqlines.get))
            dicfreqlines.pop(max(dicfreqlines, key=dicfreqlines.get), None)
            counter += 1

        counter = 0
        file.seek(0)
        x = file.readline()
        while (x != ''):
            if counter in maxfrequency:
                f_cache.write(x)
            else:
                newfile.write(x)
            x = file.readline()
            counter += 1

        f_cache.close()
        file.close()
        newfile.close()

    def print_messege(self, total_time):
        self.message = self.message + "The size of the cache: {0:,} bytes\n\n" \
                                      "The size of the index: {1:,} bytes\n\n" \
                                      "The total time of the process: {2:,} seconds".format(
            os.path.getsize("{0}cache".format(self.path)),
            os.path.getsize(self.path + "new_merged_terms") + os.path.getsize(self.path + "merged_docs_postings.txt"),
            round(total_time))

        info = Tk()
        info.title("Information")
        info.geometry("300x300")
        w = Label(info, text=self.message)
        w.pack()

        info.mainloop()
