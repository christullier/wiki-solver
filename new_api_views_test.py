import json
import requests
name = "Avengers_(comics)"
name2 = "Harry_Potter"
multiple_names = "Avengers_(comics)|Harry_Potter"
DEBUG = False

# url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/" + name + "/monthly/20200101/20200201"

# limit 50 titles per query
php_url = "https://en.wikipedia.org/w/api.php?action=query&prop=pageviews&titles=" + multiple_names + "&format=json"

headers = {
    'User-Agent': 'wikipedia game solver',
    'From' : 'cdtv1473@gmail.com'
}
response = requests.get(php_url, headers=headers)

content = response.text

# print(content)

json_object = json.loads(content)
query_object = (json_object['query'])
page_object = query_object['pages']
# print(object3)
for page_id in page_object:
    title = (page_object[page_id]['title'])
    print(title)
    sum = 0
    for date in (page_object[page_id]['pageviews']):
        daily_viewcount = page_object[page_id]['pageviews'][date]
        if DEBUG == True: 
            print("date {}:\tviews: {}".format(date, daily_viewcount))
        sum += daily_viewcount
    
    print(sum)
        

# print(json.dumps(object3)[1])





# json_object = json.loads(content)
# data = json.dumps(json_object)
# print(data[data.find("\"title\": "):])
