import json
import requests

# wiki-api likes their headers
headers = {
'User-Agent': 'wikipedia game solver',
'From' : 'cdtv1473@gmail.com'
}

# wiki api call to get all the links on a wikipedia page (left node)
def api_forwardlinks(article_title):
    links = []
    api="https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit=max&format=json&titles=" + article_title
    json_object = _request_json(api)
    page = _page_obj(json_object)

    for id in page:
        for title in page[id]['links']:
            article = title['title']
            links.append(article)

    return links

# wiki-api call to get all backlinks on a page (right node)
def api_backlinks(article_title):
    links = []
    api="https://en.wikipedia.org/w/api.php?action=query&prop=linkshere&lhlimit=max&format=json&titles=" + article_title
    json_object = _request_json(api)
    page = _page_obj(json_object)
    for id in page:
        for title in page[id]['linkshere']:
            article = title['title']
            links.append(article)

    return links

# input a list of articles and returns a dictionary of with format {title : viewcount}
# gets pageviews from last 60 days
def api_views(article_list):
    titles = "|".join(article_list)
    api = "https://en.wikipedia.org/w/api.php?action=query&prop=pageviews&format=json&pvipcontinue&titles=" + titles
    json_object = _request_json(api)
    views_dict = {}

    print(".", end='', flush = True)
    
    # api tag that lets us know if we need to make the request again (seems like api caches the result for us?)
    while 'continue' in json_object:
        json_object = _request_json(api)
    
    page = _page_obj(json_object)
    
    for id in page:
        title = page[id]['title']
        # skips wiki, category, help, and user articles
        if not (title.startswith("Wikipedia:") or title.startswith("Category:") or title.startswith("Help:") or title.startswith("User:") or title.startswith("Template:") or title.endswith("(disambiguation)")):
            pageviews = page[id]['pageviews']
            total_views = 0
            # pagevies are separated by day, summed here
            for date in pageviews:
                daily_views = pageviews[date]
                
                if daily_views == None:
                    total_views += 0
                else:
                    total_views += daily_views

            views_dict[title] = total_views
            
    return views_dict

# does request and returns json object, mostly for cleaner code
def _request_json(api_call):
    response = requests.get(api_call, headers=headers)
    content = response.text
    return(json.loads(content))

# also here for cleaner code
def _page_obj(json_object):
    query_object = json_object['query']
    return(query_object['pages'])
