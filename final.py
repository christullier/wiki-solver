import json, requests



# make links become children as soon as they're made?
# make sure that self.views is not None


class Article():
    def __init__(self, article_name):
        if article_name.startswith("https://") or article_name.startswith("en.wikipedia.org"):
            self.name = article_name.rsplit('/', 1)[-1]
        else:
            self.name = article_name

        # list of links
        self.links = self._get_links(self.name)

        # # of views
        self.views = self._get_views(self.links[:5])

    def _get_links(self, article_name):
        sub_links = []
        page_object = self._get_request(article_name)
        # print(page_object)
        for page_id in page_object:
                # main_title = page_object[page_id]['title']
                for title in (page_object[page_id]['links']):
                    sub_article = title['title']
                    sub_links.append(sub_article)

        return sub_links

    
    def _get_views(self, article_list):
        page_object = self._get_request(article_list)
        for page_id in page_object:
            title = (page_object[page_id]['title'])
            print(title)
            sum = 0
            for date in (page_object[page_id]['pageviews']):
                daily_viewcount = page_object[page_id]['pageviews'][date]
                sum += daily_viewcount
            
            print(sum)


    
    # article_list can be a list of one
    # returns page_object to be looped over
    def _get_request(self, article_list):
        # from _get_list
        if type(article_list) == list:
            titles = "|".join(article_list)
            php = "https://en.wikipedia.org/w/api.php?action=query&prop=pageviews&format=json&titles=" + titles
        # from _get_views
        elif (type(article_list) == str):
            title = article_list
            php="https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit=max&format=json&titles=" + title
        
        headers = {
            'User-Agent': 'wikipedia game solver',
            'From' : 'cdtv1473@gmail.com'
        }
        # print(php)
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
    # print(a.links)
    print(a.views)
