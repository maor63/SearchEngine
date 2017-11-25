from os import listdir

from bs4 import BeautifulSoup as BS

from Document import Document


class ReadFile:
    def read_docs(self, file_path):
        docs = []
        file = open(file_path)
        xml = BS(file, "lxml")
        documents = xml.find_all("doc")
        for document in documents:
            try:
                d = Document()
                d.id = document.find('docno').text
                text = document.find('text').text
                if text is None:
                    d.text = document.find('dateline').text
                else:
                    d.text = text
                docs.append(d)
            except Exception:
                pass

        return docs

    def read_files(self, path):
        allSubFolders = listdir(path)
        docs = []
        i = 1
        for currfolder in allSubFolders:
            msg = "\r Read file {0}/{1}".format(str(i), len(allSubFolders))
            print(msg, end="")
            i += 1
            docs.extend(self.read_docs(path + currfolder + "/" + currfolder))
            # self.read_docs(path + currfolder + "/" + currfolder)

        return docs

