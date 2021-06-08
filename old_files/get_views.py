import wikipedia as w
from mwviews.api import PageviewsClient
from operator import itemgetter
import pageviewapi

url = "https://en.wikipedia.org/wiki/Avengers_(comics)"


article_name = url.rsplit('/', 1)[-1]


p = PageviewsClient(user_agent = '<cdtv1473@gmail.com>, coding a program to connect two wiki pages')
dict_list = p.article_views('en.wikipedia', article_name).values()
# b = a.values()
# print(b)
views_list = list(map(itemgetter(article_name), dict_list))
# print(c)
tot_views = (sum(views_list[:-1]))
print(tot_views)

