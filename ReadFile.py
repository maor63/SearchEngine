import re
import os

from Document import Document
from Parser import Parser


class ReadFile:
    def __init__(self):
        self.text_tags = re.compile("\[.*]|<.*>")
        self.parser = Parser("")

    def read_files(self, path, threshold=1000):
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
            if len(docs) >= threshold:
                yield docs
                docs = []

        return docs

    def read_docs_from_FB_file(self, file_path):
        return self.read_from_file(self.remove_language_artical_type_rows, file_path)

    def read_docs_from_FT_file(self, file_path):
        return self.read_from_file(self.remove_redundant_sings, file_path)

    def read_docs_from_LA_file(self, file_path):
        return self.read_from_file(self.remove_p_tags, file_path)

    def read_from_file(self, clean_fn, file_path):
        docs = []
        if not os.path.exists(file_path):
            return docs
        file = open(file_path)
        file_text = file.read()
        raw_docs = file_text.split("</DOC>\n")
        for raw_doc in raw_docs:
            doc = self.create_doc_from_raw(raw_doc)
            if doc is not None:
                doc = clean_fn(doc)
                docs.append(doc)
        file.close()
        return docs

    def create_doc_from_raw(self, raw_doc):
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

    def remove_p_tags(self, doc):
        # text = doc.text.split("<P>\n</P>")
        # text[0] = text[0].replace("<P>\n", "")
        # text[len(text) - 1] = text[len(text) - 1].replace("</P>", "")
        # doc.text = "\n".join(text)
        doc.text = self.text_tags.sub('', doc.text)
        return doc

    def remove_language_artical_type_rows(self, doc):
        text = self.text_tags.sub('', doc.text)
        text_rows = text.split("\n")
        if text_rows[0].startswith("Language:") and text_rows[1].startswith("Article Type:"):
            text_rows = text_rows[2:]
            doc.text = "\n".join(text_rows)
        else:
            doc.text = text
        doc.text = doc.text.strip()
        return doc

    def remove_redundant_sings(self, doc):
        doc.text = self.text_tags.sub('', doc.text)
        return doc
