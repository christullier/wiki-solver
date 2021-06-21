from wiki_api import api_backlinks, api_forwardlinks, api_views
from random import random, sample

# accepts wiki links or article names formatted the same way as wiki-links
class Article():
    def __init__(self, title):
        self.title = title
        self.format_title() # if title is in link format, this fixes it

        self.parent = None
        self.child = None

        self.views_dict = None # stores views information in this format: {title : views} 
         
        self.links = [] # forwarlinks or backlinks go here depending on solver() in main.py
    
    # links parent to child and vice versa (used in solver())
    def __call__(self, other):
        self.child = other
        other.parent = self

    # formats title if it's a url
    def format_title(self):
        if self.title.startswith("https://") or self.title.startswith("en.wikipedia.org"):
            self.title = self.title.rsplit('/', 1)[-1]

    # left nodes will use this
    def forwardlinks(self):
        self.links = api_forwardlinks(self.title)

    # right nodes will use this
    def backlinks(self):
        self.links = api_backlinks(self.title)

    def get_views_dict(self):
        random_links = self._random_links()
        self.views_dict = api_views(random_links)
    
    # returns a set of random links to get the views of
    def _random_links(self):
        sample_size = 49 # the sample size is 49 because 50 is the most titles you can have in one api call (we append self lower down)
        # if there are less than 49 links on an article's page
        if sample_size > len(self.links):
            sample_size = len(self.links)
        
        random_links = sample(self.links, sample_size)

        # if the previous article was included, skip it 
        # keeps it from getting 'stuck' on a popular article
        # # this saves a surprsing amount of time lol
        if self.child != self.title or self.parent != self.title:
            random_links.append(self.title)
        
        return random_links

    # returns title with most views
    def best_link(self):
        best = ""
        views = 0
        # seemingly-unnecessary for loop here because I couldn't find a convenient way to get the 'title' from the views_dict
        # it doesn't add that much time anyway
        for title in self.views_dict:
            if self.views_dict[title] > views:
                views = self.views_dict[title]
                best = title

        return best

    
