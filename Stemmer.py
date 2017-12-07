from nltk.stem.snowball import EnglishStemmer, PorterStemmer
from collections import defaultdict, Counter
# from nltk.stem.porter import PorterStemmer


class Stemmer:
    def __init__(self):
        self.stemmer = EnglishStemmer()

    def stem(self, terms_dict):
        new_term_dict = Counter()
        for term in terms_dict:
            stemed_term = self.stemmer.stem(term)
            new_term_dict[stemed_term] += terms_dict[term]
        return dict(new_term_dict)

    def stem_list(self, terms):
        new_term_dict = defaultdict(int)
        for term_dict in terms:
            for term in term_dict:
                stemed_term = self.stemmer.stem(term)
                new_term_dict[stemed_term] += term_dict[term]
        return dict(new_term_dict)
