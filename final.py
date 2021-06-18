import json, requests, random, time
# 28 gets stuck on emma watson and clint eastwood
random.seed(29)
DEBUG = False

# make links become children as 8oon as they're made?
# make sure that self.views is not None


class Article():
    def __init__(self, article_name, direction = None):
        if article_name.startswith("https://") or article_name.startswith("en.wikipedia.org"):
            self.name = article_name.rsplit('/', 1)[-1]
        else:
            self.name = article_name
        self.direction = direction
        self.links = self._get_links(self.name, direction)     # list of links
        self.views = None   # number of views for this article

        # gets number of views for self and children article in the same call
        self.sample_size = 49
        if self.sample_size > len(self.links):
            self.sample_size = len(self.links)
        self.random_links = random.sample(self.links, self.sample_size)
        self.random_links.append(self.name)
        
        self.parent = None
        self.best_child = None

    #? may need an uplink function?
    # links the parent to the child
    def __call__(self, child):
        self.best_child = child
        child.parent = self

    def _wiki_format(self, article_title):
        return article_title.replace(" ", "_")

    def _get_links(self, article_name, direction):
        sub_links = []
        page_object = self._get_request(article_name, direction)
        for page_id in page_object:
                if 'links' in page_object[page_id]:
                    for title in (page_object[page_id]['links']):
                        sub_article = title['title']
                        sub_links.append(sub_article)
                else:
                    for title in (page_object[page_id]['linkshere']):
                        sub_article = title['title']
                        sub_links.append(sub_article)
        return sub_links
    
    def _get_best_sub_article(self, article_list):
        page_object = self._get_request(article_list)

        max_views = 0
        max_title = ""
        # print(page_object)
        for page_id in page_object:
            title = (page_object[page_id]['title'])
            if DEBUG == True: 
                print(title)
            sum = 0
            for date in (page_object[page_id]['pageviews']):
                
                daily_viewcount = page_object[page_id]['pageviews'][date]
                
                # in case there are no views
                if daily_viewcount == None:
                    sum += 0
                else:
                    sum += daily_viewcount
                sum += 0
            
            if self._wiki_format(title) == self.name:
                self.views = sum
            if DEBUG == True:
                print(sum)
            if sum > max_views:
                max_views = sum
                max_title = title

        # print(max_title)
        # print(max_views)
        # # self.best_child = (max_title)              
        # print(">")
        return max_title
    
    # article_list can be a list of one
    # returns page_object to be looped over
    def _get_request(self, article_list, direction = None):

        # if it's a list it's from _get_views
        if type(article_list) == list:
            titles = "|".join(article_list)
            # api call to get pageviews
            api = "https://en.wikipedia.org/w/api.php?action=query&prop=pageviews&format=json&pvipcontinue&titles=" + titles

        # if it's not a list, it's from _get_links, assume single string
        elif direction == "l":
            title = article_list
            # api to get page links
            api="https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit=max&format=json&titles=" + title
        
        elif direction == "r":
            title = article_list
            api="https://en.wikipedia.org/w/api.php?action=query&prop=linkshere&lhlimit=max&format=json&titles=" + title

        headers = {
            'User-Agent': 'wikipedia game solver',
            'From' : 'cdtv1473@gmail.com'
        }
        response = requests.get(api, headers=headers)
        content = response.text

        json_object = json.loads(content)

       
        # this checks to see if json_object has a 'continue' when getting the number of views 
        if type(article_list) == list:
            while 'continue' in json_object:
                new_response = requests.get(api, headers=headers)
        
                new_content = new_response.text
                json_object = json.loads(new_content)

                # print('.')

        # time.sleep(.5)
        query_object = json_object['query']
        page_object = query_object['pages']
    
        return page_object

    def printer(self):
        current = self
        print(current.name)

        while current.best_child is not None:
            current = current.best_child
            print(current.name)
            # time.sleep(1)

    @staticmethod
    def solver(left, right):
        # check if lists match up
        for item in left.links:
            if item in right.links:
                new = Article(item, 'l')
                left(new)
                new(right)
                return
        
        # get best children/parents
        left.best_child = Article(left._get_best_sub_article(left.random_links), "l")
        left(left.best_child)


        right.parent = Article(right._get_best_sub_article(right.random_links), 'r')
        right.parent(right)

        Article.solver(left.best_child, right.parent)

if __name__ == "__main__":
    name = "Ghidra"
    name2 = 'photosynthesis'
    a = Article(name, 'l')
    b = Article(name2, 'r')

    print(a.best_child)
    print(len(a.random_links))
    # print(len(a.links))
    # print(len(b.links))

    Article.solver(a, b)
    # print(a.name)
    # print(a.best_child.name)
    # print(a.best_child.best_child.name)
    a.printer()
