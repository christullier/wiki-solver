import wikipedia as w
from mwviews.api import PageviewsClient
from operator import itemgetter
import random
import time

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % \
                (method.__name__, (te - ts) * 1000))
        return result
    return timed


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
        self.links = random.sample(self._get_links(), 20)
        # self.links = self._get_links()[:5]

    def __bool__(self, other):
        if self.name == other.name:
            return True
        else:
            return False

    #? may need an uplink function?
    # links the parent to the child
    def __call__(self, child):
        self.child = child
        child.parent = self
        # links on page
        # best link

    # print function that goes along the chain
    
    # input a title w/ spaces and return it w/ spaces replaced with underscores
    def _wiki_format_title(self, article_title):
        return article_title.replace(" ", "_")

    # @timeit
    def _get_links(self):
        links_temp = w.WikipediaPage(self.name).links
        new_links = [self.name]
        # for i in range(len(links_temp)):
        for i in range(len(links_temp)):
            if "disambiguation" not in links_temp[i]:
                new_links.append(self._wiki_format_title(links_temp[i]))
        # appending self.name to keep the current article if it's view count is higher
        return new_links
    
    # @timeit
    def find_best_item(self): 
        views_list = []
        for i in range(len(self.links)):
            if self.name != self.links[i]:
                views_list.append(Article(self.links[i]).views)
        print("views_list: {}".format(views_list))
        max_views = max(views_list)
        index = views_list.index(max_views)
        return Article(self.links[index])
        
    # need an exception for pages that don't exist
    # @timeit
    def _get_views(self):
        self.p = PageviewsClient(user_agent = '<cdtv1473@gmail.com>, coding a program to connect two wiki pages')
        try:
            self.dict_list = self.p.article_views('en.wikipedia', self.name).values()
        except:
            # sets broken links # of views to 1 so it's ranked low, but not zero
            self.dict_list = 1
        
        # Abomination (comics) breaks this for some reason - how'd it get a space?
        new_name = self._wiki_format_title(self.name)
        
        self.views_list = list(map(itemgetter(self._wiki_format_title(self.name)), self.dict_list))



        return sum(filter(None, self.views_list[:-1]))

    @staticmethod
    def solve(left, right):
        print("start: {}".format(left.name))
        print("end: {}".format(right.name))

        if left == right:
            # this is here just so we can test stuff
            if right.child == None:
                right.child = right

            # assigns the right's children to the left article because they're the same
            left(right.child)
            return

        else:
            left_child = left.find_best_item()
            right_parent = right.find_best_item()
            left(left_child), right_parent(right)
            return Article.solve(left_child, right_parent)
            


    @staticmethod
    def print_trace(article):
        print(article.name)
        if article.child != None:
            Article.print_trace(article.child)
        else:
            quit()

if __name__ == "__main__":
    start = "https://en.wikipedia.org/wiki/Avengers_(comics)"
    end = "Harry_Potter"

    a = Article(start)
    b = Article(end)
    # a.child = a

    Article.solve(a, b)
    Article.print_trace(a)

    # print("a_name: " + a.name)
    # print("a_views: {}".format(a.views))
    # print("best_child: {}".format(a.find_best_item()))

    # print("b_name: " + b.name)
    # print("b_views: {}".format(b.views))
    # print("best_child: {}".format(b.find_best_item()))
