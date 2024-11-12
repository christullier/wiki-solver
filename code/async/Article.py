from random import sample
import asyncio
from wiki_api import *


# accepts wiki links or article names formatted the same way as wiki-links
class Article:
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
    async def forwardlinks(self):
        try:
            self.links = await api_forwardlinks(self.title)
        except:
            asyncio.set_event_loop(asyncio.ProactorEventLoop())
            Exception("No forwardlinks")
    # right nodes will use this
    async def backlinks(self):
        try: 
            self.links = await api_backlinks(self.title)
        except:
            asyncio.set_event_loop(asyncio.ProactorEventLoop())
            Exception("No backlinks")

    async def get_views_dict(self):
        # if there isn't a valid forwarlink or backlink, print error message and exit
        if len(self.links) == 0:
            asyncio.set_event_loop(asyncio.ProactorEventLoop())
            if self.parent is None:
                # Exception(f"\n'{self.title}' has no valid backlinks, try a different set of links")
                exit(f"\n'{self.title}' has no valid backlinks, try a different set of links")
            elif self.child is None:
                exit(f"\n'{self.title}' has no valid forwardlinks, try a different set of links")
            else:
                exit(f"\n'{self.title}' has no valid links, try a different set of links")
    
        random_links = self._random_links()
        self.views_dict = await api_views(random_links)

    # returns a set of random links to get the views of
    def _random_links(self):
        sample_size = 20 # the sample size is 49 because 50 is the most titles you can have in one api call (we append self lower down)
        # if there are less than 49 links on an article's page
        if sample_size > len(self.links):
            sample_size = len(self.links)
        
        random_links = sample(self.links, sample_size)

        # the first article won't have a parent or child
        if self.child is not None and self.parent is not None:
            # if the previous article was included, skip it 
            # keeps it from getting 'stuck' on a popular article
            if (self.child.title != self.title and self.parent is None) or (self.parent.title != self.title and self.child is None):
                random_links.append(self.title)
        
        return random_links

    # returns title with most views
    def best_link(self):
        best = ""
        views = 0
        # seemingly-unnecessary for loop here because I couldn't find a convenient way to get the 'title' from the views_dict
        # it doesn't add that much time right?
        for title in self.views_dict:
            if self.views_dict[title] > views:
                views = self.views_dict[title]
                best = title

        return best

    
