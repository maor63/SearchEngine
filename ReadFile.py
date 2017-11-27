from os import listdir

from Document import Document


class ReadFile:
    def read_files(self, path):
        allSubFolders = listdir(path)
        docs = []
        i = 1
        for currfolder in allSubFolders:
            msg = "\r Read file {0}/{1}".format(str(i), len(allSubFolders))
            print(msg, end="")
            i += 1
            if currfolder.startswith("FB"):
                self.read_docs_from_FB_file(path + currfolder + "/" + currfolder)
            elif currfolder.startswith("FT"):
                self.read_docs_from_FT_file(path + currfolder + "/" + currfolder)
            else:
                self.read_docs_from_LA_file(path + currfolder + "/" + currfolder)

        return docs

    def read_docs_from_FB_file(self, file_path):
        return self.read_from_file(lambda d: d, file_path)

    def read_docs_from_FT_file(self, file_path):
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
        e_doc_id = raw_doc.find("</DOCNO>", s_doc_id + 6)
        doc_id = raw_doc[s_doc_id + 7:e_doc_id].strip()
        d.id = doc_id

        s_doc_text = raw_doc.find("<TEXT>", e_doc_id + 7)
        e_doc_text = raw_doc.find("</TEXT>", s_doc_text + 6)
        if s_doc_text == -1:
            return None
        d.text = raw_doc[s_doc_text + 6: e_doc_text].strip()
        return d

    def fix_text(self, doc):
        text = doc.text.split("<P>\n</P>")
        text[0] = text[0].replace("<P>\n", "")
        text[len(text) - 1] = text[len(text) - 1].replace("</P>", "")
        doc.text = "\n".join(text)
        return doc
