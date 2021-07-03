import asyncio
import sys
from random import random, seed
from time import sleep, time

from Article import *


# left node is starting and right is ending
async def solve(left, right):
    # get links here because the for loop won't work without them
    await asyncio.gather(
        left.forwardlinks(),
        right.backlinks()
    )

    # check if lists match up
    for item in left.links:
        # if there's a match, it links the two ends of the linked list
        # if match is found, the program won't get views, which saves time (neat!)
        if item in right.links:
            new = Article(item)
            left(new)
            new(right)
            return

    # asynchronously get both sides
    await asyncio.gather(
        left.get_views_dict(),
        right.get_views_dict()
    )

    left.child = Article(left.best_link())
    right.parent = Article(right.best_link())
    
    left(left.child) # callable that links parent(child)
    right.parent(right) # right is the child in this case because we're using backlinks
    print()
    
    print(f"\n{left.child.title} <---> {right.parent.title}", flush = True)
    # print(f"right: {right.parent.title}", flush = True)
    # print(".", end='', flush = True)


    await solve(left.child, right.parent)

# prints list of articles with the game's solution (you gotta solve first solving)
def printer(start_article):
    print("\n")
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
        cmd1 = str(sys.argv[1])
        cmd2 = str(sys.argv[2])
    else:
        cmd1 = input('starting link: ')
        cmd2 = input('ending link: ')
    
    if cmd1 != "":
        name1 = cmd1
    if cmd2 != "":
        name2 = cmd2
    
    start = Article(name1)
    end = Article(name2)

    print("Searching")

    asyncio.run(solve(start, end))

    printer(start)
