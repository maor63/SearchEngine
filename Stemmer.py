from collections import defaultdict, Counter
from nltk.stem.snowball import EnglishStemmer


class Stemmer:
    def __init__(self):
        self.was_stemed = defaultdict()
        self.stemmer = EnglishStemmer()

    def stem(self, terms_dict):
        new_term_dict = Counter()
        for term in terms_dict:
            if term in self.was_stemed:
                stemed_term = self.was_stemed[term]
            elif term[0].isdigit() or len(term) <= 3:
                stemed_term = term
            else:
                stemed_term = self.stemmer.stem(term)
                self.was_stemed[term] = stemed_term
            new_term_dict[stemed_term] += terms_dict[term]
        return dict(new_term_dict)

    def stem_list(self, terms):
        new_term_dict = defaultdict(int)
        for term_dict in terms:
            for term in term_dict:
                stemed_term = self.stemmer.stem(term)
                new_term_dict[stemed_term] += term_dict[term]
        return dict(new_term_dict)
