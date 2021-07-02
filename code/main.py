import sys
from time import sleep, time

from Article import *


# left node is starting and right is ending
def solve(left, right):
    # get links here because the for loop won't work without them
    left.forwardlinks()
    right.backlinks()

    # check if lists match up
    for item in left.links:
        # if there's a match, it links the two ends of the linked list
        # if match is found, the program won't get views, which saves time (neat!)
        if item in right.links:
            new = Article(item)
            left(new)
            new(right)
            return

    left.get_views_dict()
    left.child = Article(left.best_link())
    # print(".", end='', flush = True)
    # print(f"{left.child.title=}", flush = True)
    left(left.child) # callable that links parent(child)

    right.get_views_dict()
    right.parent = Article(right.best_link())
    # print(".", end='', flush = True)

    # print(f"{right.parent.title=}", flush = True)
    right.parent(right) # right is the child in this case because we're using backlinks
    solve(left.child, right.parent)
    print()


# prints list of articles with the game's solution (you gotta solve first solving)
def printer(start_article):
    print()
    current = start_article
    print(current.title)

    # keeps printing as long as there's children
    while current.child is not None:
        current = current.child
        # if current.title != current.parent.title: # prevents from printing duplicates
        print(current.title)
    
if __name__ == "__main__":
    name1 = "Avengers (comics)" # starting article
    name2 = "The Room" # finish article

    if len(sys.argv) > 1:
        ui1 = str(sys.argv[1])
        ui2 = str(sys.argv[2])
    else:
        ui1 = input('starting link: ')
        ui2 = input('ending link: ')
    
    if ui1 != "":
        name1 = ui1
    if ui2 != "":
        name2 = ui2
    
    start = Article(name1)
    end = Article(name2)

    print("Searching")

    solve(start, end)

    printer(start)
