import json, requests

class Article():
    def __init__(self, article_name):
        if article_name.startswith("https://") or article_name.startswith("en.wikipedia.org"):
            self.name = article_name.rsplit('/', 1)[-1]
        else:
            self.name = article_name

        # list of links
        self.links = self._get_links(self.name)

        # # of views
        self.views = self._get_views(self.name)

    def _get_links(self, article_name):
        sub_links = []
        page_object = self._get_request(article_name, "links")
        # print(page_object)
        for page_id in page_object:
                # main_title = page_object[page_id]['title']
                for title in (page_object[page_id]['links']):
                    sub_article = title['title']
                    sub_links.append(sub_article)

        return sub_links

    
    def _get_views(self, article_list):
        pass

    
    # article_list can be a list of one
    # returns page_object to be looped over
    def _get_request(self, article_list, prop_type, limit = "max"):
        if type(article_list) == list > 1:
            titles = "|".join(article_list)
        elif (type(article_list) == str):
            titles = article_list
        
        headers = {
            'User-Agent': 'wikipedia game solver',
            'From' : 'cdtv1473@gmail.com'
        }
        php="https://en.wikipedia.org/w/api.php?action=query&prop=" + prop_type + "&pllimit="+ limit +"&format=json&titles=" + titles
        print(php)
        response = requests.get(php, headers=headers)
        content = response.text
        json_object = json.loads(content)
        query_object = json_object['query']
        page_object = query_object['pages']
    
        return page_object




if __name__ == "__main__":
    name = "Avengers_(comics)"
    a = Article(name)

    print(a.name)
    print(a.links)
