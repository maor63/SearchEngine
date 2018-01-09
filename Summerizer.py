from collections import Counter

import math

from Parser import Parser
from Stemmer import Stemmer


class Summerizer():
    def __init__(self, stop_word_path):
        self.parser = Parser(stop_word_path)
        self.stemmer = Stemmer()
        self.term_dict = {}
        self.N = 0

    def get_importent_sentences(self, doc, limit, stem=False):
        self.term_dict = self.parser.parse(doc.text)
        if stem:
            self.term_dict = self.stemmer.stem(self.term_dict)
        optimal_sentenc = list(map(lambda t: t[0], self.term_dict.most_common(13)))
        optimal_sentenc = optimal_sentenc[3:]
        text = doc.text
        text = text.replace('!', '.')
        text = text.replace('?', '.')
        sentences = text.split('.')
        self.N = len(sentences)
        senteces_counter = Counter()
        for sentence in sentences:
            sentence_terms = self.parser.parse(sentence)
            if len(sentence_terms) > 3:
                senteces_counter[sentence] = self.calculate_cossim(optimal_sentenc, sentence_terms)
        most_common_sentences = list(map(lambda s: s[0], senteces_counter.most_common(limit)))
        return most_common_sentences

    def calculate_tfidf(self, word, sentence):
        frec = Counter(sentence)[word]
        D = len(sentence)
        tf = frec / D
        df = self.term_dict[word]
        idf = math.log2(self.N / df)
        return tf * idf

    def calculate_cossim(self, query, sentence):
        innerproduct = 0
        for word in query:
            word_w = self.calculate_tfidf(word, sentence)
            innerproduct += word_w
        denominator = math.sqrt(len(query) * len(sentence))

        return innerproduct / denominator
