import wikipedia
import requests, urllib.request
from bs4 import BeautifulSoup
import json

"""
The idea is each article is a class with its own info
 # url
 # title of the article
 # number of views
 #? list of links on the page?

# right now do everything manually and combine it later

"""
class Article():
    def __init__(self, url):
        self.url = url
        # use BS to get title
        self.title = self._url_to_title(url)
        # use views function to get views
        self.views = self._get_article_views(self.url.rsplit('/', 1)[-1])
    
    
    # * gets title
    def _url_to_title(self, article_url):
        self.response = requests.get(url=article_url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.title = self.soup.find(id="firstHeading")
        print(self.title.string)
        return self.title.string

    # * function to get views
        # * separate into sub private functions

    def _get_article_views(self, article_title):
        self.api_article_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/" + article_title + "/monthly/20210101/20210401"
        self.full_json_file = (self.api_article_url)
        return self._views_from_json(self.full_json_file)

    def _views_from_json(self, data):
        self.my_data = json.load(data)
        for i in self.my_data['items']:
            print('views: {}'.format(i['views']))

    def _to_file(self, filename, text):
        self.f = open(filename, "w")
        self.f.write(text)
        self.f.close()


    # fn to get next 'best' article (returns an article object)


# main
if __name__ == "__main__":

    url = "https://en.wikipedia.org/wiki/Harry_Potter"
    url2 = "https://en.wikipedia.org/wiki/Avengers_(comics)"


    my_obj = Article(url)
    print(my_obj.views)
