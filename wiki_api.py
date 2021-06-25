import json, requests

# wiki-api likes their headers
headers = {
'User-Agent': 'wikipedia game solver',
'From' : 'cdtv1473@gmail.com'
}

# wiki api call to get all the links on a wikipedia page (left node)
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

# wiki-api call to get all backlinks on a page (right node)
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

# input a list of articles and returns a dictionary of with format {title : viewcount}
# gets pageviews from last 60 days
def api_views(article_list):
    titles = "|".join(article_list)
    api = "https://en.wikipedia.org/w/api.php?action=query&prop=pageviews&format=json&pvipcontinue&titles=" + titles
    json_object = _json_object(api)
    views_dict = {}
    
    # api tag that lets us know if we need to make the request again (seems like api caches the result for us?)
    while 'continue' in json_object:
        json_object = _json_object(api)
    
    page = _page_obj(json_object)
    
    for id in page:
        title = page[id]['title']
        if not title.startswith("Wikipedia:") or title.startswith("Category:") or title.startswith("Help:"):
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
        # else:
        #     print("ignored: {}".format(title)) # remove this before pushing
    return views_dict

# for cleaner code
def _json_object(api_call):
    response = requests.get(api_call, headers=headers)
    content = response.text
    return(json.loads(content))

# also here for cleaner code
def _page_obj(json_object):
    query_object = json_object['query']
    return(query_object['pages'])
