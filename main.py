from Article import *

# left node is starting and right is ending
def solve(left, right):
    # get links here because the for loop won't work without them
    left.forwardlinks()
    right.backlinks()

    # check if lists match up
    for item in left.links:
        if item in right.links:
            new = Article(item)
            left(new)
            new(right)
            return

    # makes me happy that if it finds a match, the program won't get views
    left.get_views_dict()
    left.child = Article(left.best_link())
    left(left.child) # callable that links parent(child)

    right.get_views_dict()
    right.parent = Article(right.best_link())
    right.parent(right) # right is the child in this case because we're using backlinks

    solve(left.child, right.parent)


# prints list of articles with the game's solution (you gotta solve first solving)
def printer(start_article):
    current = start_article
    print(current.title)

    # keeps printing as long as there's children
    while current.child is not None:
        current = current.child
        print(current.title)
    
if __name__ == "__main__":
    name1 = "Avengers (comics)" # starting article
    name2 = "The Room" # finish article

    start = Article(name1)
    end = Article(name2)

    solve(start, end)

    printer(start)
