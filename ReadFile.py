import os
import re

from Document import Document
from Parser import Parser


class ReadFile:
    def __init__(self):
        self.text_tags = re.compile("\[.*]|<.*>")
        self.parser = Parser("")

    def count_docs(self, path):
        '''
        return the count of the files in a given @path
        '''
        path = path + "corpus/"
        all_sub_folders = os.listdir(path)
        return sum(map(lambda x: 1, all_sub_folders))

    def read_files(self, path, threshold=5):
        '''
        create an iterator of the files in the given path
        :param path: files paths
        :param threshold: the amount of files returned each iteration, batch limit
        :return: iterator that returns batch of files
        '''
        path = path + "corpus/"
        all_sub_folders = os.listdir(path)
        docs = []
        i = 1
        for curr_folder in all_sub_folders:
            msg = "Read file {0}/{1} : {2}".format(str(i), len(all_sub_folders), curr_folder)
            print(msg)
            i += 1
            if curr_folder.startswith("LA"):
                d = self.read_docs_from_LA_file(path + curr_folder + "/" + curr_folder)
            elif curr_folder.startswith("FB"):
                d = self.read_docs_from_FB_file(path + curr_folder + "/" + curr_folder)
            else:
                d = self.read_docs_from_FT_file(path + curr_folder + "/" + curr_folder)
            docs.extend(d)
            if i % threshold == 0:
                yield docs
                docs = []
        yield docs

    def read_docs_from_FB_file(self, file_path):
        '''
        read FB file type
        '''
        return self.read_from_file(self.remove_language_artical_type_rows, file_path)

    def read_docs_from_FT_file(self, file_path):
        '''
        read FT file type
        '''
        return self.read_from_file(self.remove_redundant_signs, file_path)

    def read_docs_from_LA_file(self, file_path):
        '''
        read LA file type
        '''
        return self.read_from_file(self.remove_redundant_signs, file_path)

    def read_from_file(self, clean_fn, file_path):
        '''
        create documents from file
        :param clean_fn: function for cleaning the text of the doc
        :param file_path: the path of the file 
        :return: the documents from the file
        '''
        docs = []
        if not os.path.exists(file_path):
            return docs
        file = open(file_path, 'r')
        file_text = file.read()
        file_text = file_text
        raw_docs = file_text.split("</DOC>\n")
        for raw_doc in raw_docs:
            doc = self.create_doc_from_raw(raw_doc)
            if doc is not None:
                doc = clean_fn(doc)
                docs.append(doc)
        file.close()
        return docs

    def create_doc_from_raw(self, raw_doc):
        '''
        take raw document and convert it to Document object
        :param raw_doc: 
        :return: 
        '''
        d = Document()
        s_doc_id = raw_doc.find("<DOCNO>")
        e_doc_id = raw_doc.find("</DOCNO>", s_doc_id + len("<DOCNO>"))
        doc_id = raw_doc[s_doc_id + len("<DOCNO>"):e_doc_id].strip()
        d.id = doc_id

        s_doc_text = raw_doc.find("<TEXT>", e_doc_id + len("</DOCNO>"))
        e_doc_text = raw_doc.find("</TEXT>", s_doc_text + len("<TEXT>"))
        if s_doc_text == -1:
            return None
        d.text = raw_doc[s_doc_text + len("<TEXT>"): e_doc_text].strip()
        return d

    def remove_language_artical_type_rows(self, doc):
        '''
        remove the "Language:" row and "Artical:" row from document text
        :param doc: document
        :return: clean document
        '''
        text = self.text_tags.sub('', doc.text)
        text_rows = text.split("\n")
        if text_rows[0].startswith("Language:") and text_rows[1].startswith("Article Type:"):
            text_rows = text_rows[2:]
            doc.text = "\n".join(text_rows)
        else:
            doc.text = text
        doc.text = doc.text.strip()
        return doc

    def remove_redundant_signs(self, doc):
        '''
        remove tags from document text
        :param doc: document
        :return: clean document
        '''
        doc.text = self.text_tags.sub('', doc.text)
        return doc

    def read_query_file(self, query_file):
        f = open(query_file, 'r')
        text = f.read()
        queries = {}
        raw_queries = text.split('</top>')[:-1]
        for raw_query in raw_queries:
            num = int(self.getDataFromTag(raw_query, "<num> Number:").strip())
            query = self.getDataFromTag(raw_query, "<title>").strip()
            queries[query] = num

        return queries

    def getDataFromTag(self, raw_query, tag):
        s = raw_query.find(tag) + len(tag)
        e = raw_query.find("\n", s)
        return raw_query[s: e]

    def save_query_results(self, query_results, path):
        pass

