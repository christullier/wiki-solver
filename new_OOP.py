import wikipedia


class Article():
    def __init__(self, article_name):
        self.name = article_name
        self.page = wikipedia.page(article_name)
        self.views = self.page.views
        self.links = 
