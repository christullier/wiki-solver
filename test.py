import wikipedia
from mwviews.api import PageviewsClient

import pageviewapi
# test
# page = wikipedia.page("Avengers_(comics)")
# print(page.links)

# page2 = wikipedia.page("Avengers: Endgame")
# print(page2.title)

p = PageviewsClient(user_agent = '<cdtv1473@gmail.com>, coding a program to connect two wiki pages')
# p.article_views('es.wikipedia', ['Fideuà', 'Paella'])
print(p.top_articles('de.wikivoyage', limit=10))
# p.article_views('en.wikipedia', 'apple')



