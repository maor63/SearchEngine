import random
import wikipedia

class WikipediaExpander:
    def expand(self, query):
        query = query .strip()
        if len(query.split(' ')) > 1:
            return query
        expended_query = [query]
        page = wikipedia.page(query)
        add_terms = 4
        if len(page.links) <= add_terms:
            expended_query.extend(page.links)
        else:
            expended_query.extend(random.sample(page.links, add_terms))
        return " ".join(expended_query)