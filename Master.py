from concurrent.futures import ThreadPoolExecutor

from Parser import Parser
from ReadFile import ReadFile


class Master:
    def __init__(self):
        self.file_reader = ReadFile()
        self.parser = Parser("./LA/stop_words.txt")

    def run_process(self):
        executor = ThreadPoolExecutor(max_workers=4)
        total_docs = self.file_reader.read_files("./LA/", 1000)
        for next_docs in total_docs:
            texts = []
            for doc in next_docs:
                texts.append(self.parse_text(doc.text))
            pass
            print("batch ended")

    def parse_text(self, text):
        return self.parser.parse(text)

