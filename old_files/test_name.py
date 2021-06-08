import wikipedia as w

def get_title(article_name):
    return(w.WikipediaPage(article_name).original_title)

print(get_title("Avengers (comics)"))
