import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Harry_Potter"
url2 = "https://en.wikipedia.org/wiki/Avengers"


def pageTitle(article_url):
	response = requests.get(url=article_url)
	soup = BeautifulSoup(response.content, 'html.parser')
	title = soup.find(id="firstHeading")
	print(title.string)
	return title.string


def pageViews(article_name):
	view_api = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/" + article_name + "/monthly/20150101/20161201"
	print view_api

pageTitle(url)
pageTitle(url2)

pageViews("harry_potter")



"""
f = open("output.txt", "w+")
f.write(title.string)
f.close()
"""
