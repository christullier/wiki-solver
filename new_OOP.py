import wikipedia as w
from mwviews.api import PageviewsClient
from operator import itemgetter

# use getter and setters for the views function so
# they 
class Article():
    def __init__(self, article_name):
        # if the input is a url
        if article_name.startswith("https://") or article_name.startswith("en.wikipedia.org"):
            self.name = article_name.rsplit('/', 1)[-1]
        else:
            self.name = article_name
        # self.name = article_name
        self.views = self._get_views()
        self.parent = None
        self.child = None
        self.links = None

    #? may need an uplink function?
    # links the parent to the child
    def __call__(self, child):
        self.child = child
        child.parent = self
        # links on page
        # best link

    # print function that goes along the chain
        
        # parent (got here from parent)
        # child (next article)
    def _get_links(self):
        links_temp = w.WikipediaPage(self.name).links
        for i in range(len(links_temp)):
            links_temp[i] = self._wiki_format_title(links_temp[i])
        self.links = links_temp

    def find_best_child(self):
        self._get_links()
        views_list = []
        for i in range(len(self.links)):
            views_list.append(Article(self.links[i]))
        return max(views_list)
        
    # need an exception for pages that don't exist
    def _get_views(self):
        self.p = PageviewsClient(user_agent = '<cdtv1473@gmail.com>, coding a program to connect two wiki pages')
        self.dict_list = self.p.article_views('en.wikipedia', self.name).values()
        self.views_list = list(map(itemgetter(self.name), self.dict_list))
        return sum(filter(None, self.views_list[:-1]))

    # input a title w/ spaces and return it w/ spaces replaced with underscores
    def _wiki_format_title(self, article_title):
        return article_title.replace(" ", "_")



if __name__ == "__main__":
    start = "https://en.wikipedia.org/wiki/Avengers_(comics)"
    end = "Harry_Potter"

    a = Article(start)
    print("a_name: " + a.name)
    print("a_views: {}".format(a.views))
    print("best_child: {}".format(a.find_best_child()))

    b = Article(end)
    print("b_name: " + b.name)
    print("b_views: {}".format(b.views))

