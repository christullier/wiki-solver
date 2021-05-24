import requests, urllib.request
from bs4 import BeautifulSoup
import json


class Article():
    def __init__(self, url):
        self.url = url
        # use BS to get title
        self.title = _url_to_title(url)
        # use views function to get views
        self.views = views
    
    
    # gets title
    def _url_to_title(article_url):
    	self.response = requests.get(url=article_url)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.find(id="firstHeading")
        print(title.string)
        return title.string

    # function to get views

    # fn to get next 'best' article (returns an article object)
