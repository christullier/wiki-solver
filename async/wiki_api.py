import asyncio
import httpx
import json

# wiki-api likes their headers
headers = {
'User-Agent': 'wikipedia game solver',
'From' : 'cdtv1473@gmail.com'
}

async def api_forwardlinks(article_title):
    """Gets the forwardlinks for an article, for use on left nodes

    Args:
        article_title (text): wiki article title

    Returns:
        list: wiki links from the title page
    """    
    links = []
    api="https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit=max&format=json&titles=" + article_title
    json_object = await _async_json_object(api)
    page = _page_obj(json_object)

    for id in page:
        for article in page[id]['links']:
            title = article['title']
            # skips wiki, category, help, and user articles
            if not (title.startswith("Wikipedia:") or title.startswith("Category:") or title.startswith("Help:") or title.startswith("User:") or title.startswith("User talk:") or title.startswith("Talk:") or title.startswith("Template:") or title.endswith("(disambiguation)")):
                links.append(title)

    return links

async def api_backlinks(article_title):
    """Gets the backlinks for an article, for use on right nodes

    Args:
        article_title (text): wiki article title

    Returns:
        list: wiki links that link to the title page
    """
    links = []
    api="https://en.wikipedia.org/w/api.php?action=query&prop=linkshere&lhlimit=max&format=json&titles=" + article_title
    json_object = await _async_json_object(api)
    page = _page_obj(json_object)

    for id in page:
        for article in page[id]['linkshere']:
            title = article['title']
            # skips wiki, category, help, and user articles
            if not (title.startswith("Wikipedia:") or title.startswith("Category:") or title.startswith("Help:") or title.startswith("User:") or title.startswith("User talk:") or title.startswith("Talk:") or title.startswith("Template:") or title.endswith("(disambiguation)")):
                links.append(title)
                
    return links

async def api_views(article_list):
    """Gets pageviews from the last 60 days for a list of 50 or less articles

    Args:
        article_list (list): a list of article titles

    Returns:
        dict: {title : viewcount} for each article in the list
    """
    titles = "|".join(article_list)
    api = "https://en.wikipedia.org/w/api.php?action=query&prop=pageviews&format=json&pvipcontinue&titles=" + titles
    json_object = await _async_json_object(api)
    views_dict = {}
    
    # api tag that lets us know if we need to make the request again (seems like api caches the result for us?)
    while 'continue' in json_object:
        json_object = await _async_json_object(api)
    
    page = _page_obj(json_object)
    
    for id in page:
        title = page[id]['title']
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

async def _async_json_object(api_call):
    """async function to make a request to the wiki api and return a json object with article information

    Args:
        api_call (text): link to the api call
    
    Returns:
        dict: json content from the api call
    """            
    async with httpx.AsyncClient() as client:
        response = await client.get(api_call, headers=headers)    
        content = response.text
        await client.aclose()
        print(".", flush = True, end = "")
        return(json.loads(content))
    

# also here for cleaner code
def _page_obj(json_object):
    """takes json input and returns a page object

    Args:
        json_object (dict): json data from api

    Returns:
        dict: json object for the 'pages' of an article
    """
    query_object = json_object['query']
    return(query_object['pages'])
