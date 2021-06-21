from wiki_api import api_backlinks, api_forwardlinks, api_views
from random import random, sample

class Article():
    def __init__(self, title):
        self.title = title
        self.format_title()

        self.parent = None
        self.child = None

        self.views_dict = None
        # either uplinks or backlinks 
        self.links = []
    
    # links parent to child and vice versa
    def __call__(self, other):
        self.child = other
        other.parent = self

    # formats title
    def format_title(self):
        if self.title.startswith("https://") or self.title.startswith("en.wikipedia.org"):
            self.title = self.title.rsplit('/', 1)[-1]

    def forwardlinks(self):
        self.links = api_forwardlinks(self.title)

    def backlinks(self):
        self.links = api_backlinks(self.title)

    def get_views_dict(self):
        random_links = self._random_links()
        self.views_dict = api_views(random_links)
    
    def _random_links(self):
        sample_size = 49
        if sample_size > len(self.links):
            sample_size = len(self.links)
        
        random_links = sample(self.links, sample_size)
        random_links.append(self.title)
        return random_links

    def best_link(self):
        best = ""
        views = 0
        for title in self.views_dict:
            if self.views_dict[title] > views:
                views = self.views_dict[title]
                best = title

        return best
                


if __name__ == "__main__":
    a = Article("The_Room")
    print(a.title)
    a.backlinks()
    a.get_views_dict()

    print(a.best_link())
    
