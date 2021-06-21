import json, requests, random, time

headers = {
'User-Agent': 'wikipedia game solver',
'From' : 'cdtv1473@gmail.com'
}

def api_forwardlinks(article_title):
    links = []
    api="https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit=max&format=json&titles=" + article_title
    json_object = _json_object(api)
    page = _page_obj(json_object)

    for id in page:
        for title in page[id]['links']:
            article = title['title']
            links.append(article)

    return links


def api_backlinks(article_title):
    links = []
    api="https://en.wikipedia.org/w/api.php?action=query&prop=linkshere&lhlimit=max&format=json&titles=" + article_title
    json_object = _json_object(api)
    page = _page_obj(json_object)
    for id in page:
        for title in page[id]['linkshere']:
            article = title['title']
            links.append(article)

    return links

# takes in a list of articles and returns a dictionary of with format {title : viewcount}
def api_views(article_list):
    titles = "|".join(article_list)
    api = "https://en.wikipedia.org/w/api.php?action=query&prop=pageviews&format=json&pvipcontinue&titles=" + titles
    json_object = _json_object(api)
    views_dict = {}
    
    while 'continue' in json_object:
        json_object = _json_object(api)
    
    page = _page_obj(json_object)
    
    for id in page:
        title = page[id]['title']
        pageviews = page[id]['pageviews']
        total_views = 0
        for date in pageviews:
            daily_views = pageviews[date]
            
            if daily_views == None:
                total_views += 0
            else:
                total_views += daily_views

        views_dict[title] = total_views
    return views_dict

def _json_object(api_call):
    response = requests.get(api_call, headers=headers)
    content = response.text
    return(json.loads(content))

def _page_obj(json_object):
    query_object = json_object['query']
    return(query_object['pages'])


if __name__ == "__main__":
    # print(api_backlinks("The_Room"))
    # api_views(["The_Room", "Avengers_(comics)"])
    # api_forwardlinks("The Room")
    pass
