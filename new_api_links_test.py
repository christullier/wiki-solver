import json, requests

title = "Avengers_(comics)"
# 1-50 or max
limit = 'max'

php="https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit="+ limit +"&format=json&titles=" + title

headers = {
    'User-Agent': 'wikipedia game solver',
    'From' : 'cdtv1473@gmail.com'
}
response = requests.get(php, headers=headers)
content = response.text
json_object = json.loads(content)
query_object = json_object['query']
page_object = query_object['pages']

for page_id in page_object:
    main_title = (page_object[page_id]['title'])
    print(main_title)
    for title in (page_object[page_id]['links']):
        # print(page_object[page_id][title])
        sub_article = title['title']
        print(sub_article)

