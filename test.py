import urllib, json
url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/foo/monthly/20150101/20161201"

response = urllib.urlopen(url)

data = json.loads(response.read())
print data


f = open("jout.json", "w+")
f.write(json.loads(response.read()))
f.close()
