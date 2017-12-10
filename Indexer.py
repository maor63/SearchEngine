import os

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

    def merge(self):
        files_names = list(filter(lambda f: "terms" in f, os.listdir(self.path)))
        files = list(map(lambda f: open(self.path + f), files_names))
        self.TermDictionary = self.merge_files("merged_terms.txt", files, self.merge_term_line)

        files_names = list(filter(lambda f: "docs" in f, os.listdir(self.path)))
        files = list(map(lambda f: open(self.path + f), files_names))
        self.DocsDictionary = self.merge_files('merged_docs.txt', files, self.merdge_doc_line)

    def merge_files(self, output_file, input_files, merge_line_fn):
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
                dictionary[term] = file_row
                file_row += 1
            output_file.flush()
            input_files = list(filter(lambda x: x.name not in files_to_delete, input_files))
        output_file.close()
        return dictionary

    def merge_term_line(self, line, sorted_lines):
        term, frec, doc_list = line.split('#')
        if term not in sorted_lines:
            sorted_lines[term] = line
        else:
            term2, frec2, doc_list2 = sorted_lines[term].split('#')
            sorted_lines[term] = '#'.join(
                [term, str(int(frec) + int(frec2)), doc_list.rstrip() + doc_list2])

    def merdge_doc_line(self, line, sorted_lines):
        doc_data = line.split('#')
        sorted_lines[doc_data[0]] = line

    def cache(self):
        f_cache = open("{0}cache".format(self.path), 'a')
        line = 0
        maxs = []
        counter = 0
        dicfreqlines = {}
        file_terms = list((filter(lambda f: "terms" in f, os.listdir(self.path))))
        file = open(self.path + file_terms[0])
        file.seek(0)
        x = file.readline()
        while (x != ''):
            term, freq, doc_list = x.split('#')
            dicfreqlines[line] = int(freq)
            line += 1
            x = file.readline()

        while (counter <= 100):
            maxs.append(max(dicfreqlines, key=dicfreqlines.get))
            dicfreqlines.pop(max(dicfreqlines, key=dicfreqlines.get), None)
            counter += 1

        f = open(self.path + file_terms[0], "r")
        lines = f.readlines()
        f.close()
        f = open(self.path + file_terms[0], "w")
        counter = 0
        for l in lines:
            if counter in maxs:
                f_cache.write(l)
            else:
                f.write(l)
            counter += 1
        f.close()
