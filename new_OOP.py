import wikipedia as w
from mwviews.api import PageviewsClient
from operator import itemgetter


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

        # links on page
        # best link

        
        # parent (got here from parent)
        # child (next article)



    def _get_views(self):
        self.p = PageviewsClient(user_agent = '<cdtv1473@gmail.com>, coding a program to connect two wiki pages')
        self.dict_list = self.p.article_views('en.wikipedia', self.name).values()
        self.views_list = list(map(itemgetter(self.name), self.dict_list))
        return sum(self.views_list[:-1])

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Avengers_(comics)"
    title = "Avengers:_Endgame"

    a = Article(url)
    print("a_name: " + a.name)
    print("a_views: {}".format(a.views))

    b = Article(title)
    print("b_name: " + b.name)
    print("b_views: {}".format(b.views))

