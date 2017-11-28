from os import listdir

from Document import Document


class ReadFile:
    def read_files(self, path):
        all_sub_folders = listdir(path)
        docs = []
        i = 1
        for curr_folder in all_sub_folders:
            msg = "\r Read file {0}/{1}".format(str(i), len(all_sub_folders))
            print(msg, end="")
            i += 1
            if curr_folder.startswith("LA"):
                self.read_docs_from_LA_file(path + curr_folder + "/" + curr_folder)
            else:
                self.read_docs_from_FB_FT_file(path + curr_folder + "/" + curr_folder)

        return docs

    def read_docs_from_FB_FT_file(self, file_path):
        return self.read_from_file(lambda d: d, file_path)

    def read_docs_from_LA_file(self, file_path):
        return self.read_from_file(self.fix_text, file_path)

    def read_from_file(self, clean_fn, file_path):
        docs = []
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

    def fix_text(self, doc):
        text = doc.text.split("<P>\n</P>")
        text[0] = text[0].replace("<P>\n", "")
        text[len(text) - 1] = text[len(text) - 1].replace("</P>", "")
        doc.text = "\n".join(text)
        return doc
