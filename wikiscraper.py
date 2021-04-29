import requests, urllib.request
from bs4 import BeautifulSoup
import json

url = "https://en.wikipedia.org/wiki/Harry_Potter"
url2 = "https://en.wikipedia.org/wiki/Avengers"


# inputs article url and outputs the page title
def pageTitle(article_url):
	response = requests.get(url=article_url)
	soup = BeautifulSoup(response.content, 'html.parser')
	title = soup.find(id="firstHeading")
	print(title.string)
	return title.string

# gets the URL name for pageviews function
def urlName(article_url):
	name = article_url.rsplit('/', 1)[-1]
	return name

# output from the wiki api is going to be in .json format
# input needs to be the URL form of the link
def pageViews(article_name):
	view_api = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/" + article_name + "/monthly/20210101/20210401"
	print(view_api)
	getJsonData(view_api)

# opens json file and gets the number of views
def jsonToViews(api_link):
    pass


# name json file after the wikipedia page maybe?
def getJsonData(link):
	with urllib.request.urlopen(link) as url: data = json.loads(url.read().decode())
	with open('jout.json', 'w') as outfile: json.dump(data, outfile, indent=4)
	# print(data)
	# return data


def openJ(filename):
	with open(filename) as json_file:
		data = json.load(json_file)
		for i in data['items']:
			print('views: {}'.format(i['views']))
			

def toFile(filename, text):
	f = open(filename, "w")
	f.write(text)
	f.close()

pageTitle(url)
pageTitle(url2)

pageViews(urlName(url2))


openJ('jout.json')

"""
f = open("output.txt", "w+")
f.write(title.string)
f.close()
"""
