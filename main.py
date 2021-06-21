from Article import *

def solve(left, right):
    left.forwardlinks()
    right.backlinks()

    # check if lists match up
    for item in left.links:
        if item in right.links:
            new = Article(item)
            left(new)
            new(right)
            return


    left.get_views_dict()
    left.child = Article(left.best_link())
    left(left.child)

    right.get_views_dict()
    right.parent = Article(right.best_link())
    right.parent(right)

    solve(left.child, right.parent)



def printer(start_article):
    current = start_article
    print(current.title)

    while current.child is not None:
        current = current.child
        print(current.title)
        # time.sleep(1)
    
if __name__ == "__main__":
    name1 = "Avengers_(comics)"
    name2 = "The_Room"

    start = Article(name1)
    end = Article(name2)

    solve(start, end)

    printer(start)
