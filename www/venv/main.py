import asyncio
import sys

from Article import *


# left node is starting and right is ending
async def solve(left, right):
    # get links here because the for loop won't work without them
    await asyncio.gather(
        left.forwardlinks(),
        right.backlinks())

    # check current left node against the end node and its parents
    r = end
    while r is not None:
        for item in left.links:
            if item in r.links:
                new = Article(item)
                left(new)
                new(r)
                return
        r = r.parent
    
    # check current right node against the start node and it's children
    l = start
    while l is not None:
        for item in right.links:
            if item in l.links:
                new = Article(item)
                l(new)
                new(right)
                return
        l = l.parent

    # asynchronously get both sides
    await asyncio.gather(
        left.get_views_dict(),
        right.get_views_dict())

    left.child = Article(left.best_link())
    right.parent = Article(right.best_link())
    
    left(left.child) # callable that links parent(child)
    right.parent(right) # right is the child in this case because we're using backlinks
    
    sys.stdout.write("\033[F")

    print()
    sys.stdout.write("\033[K")
    sys.stdout.write(f"{left.child.title} <---> {right.parent.title}")
    sys.stdout.flush()
    
    await solve(left.child, right.parent)


# prints list of articles with the game's solution (you gotta solve first solving)
def printer(start_article):
    art_list = []
    print("\n")
    current = start_article
    art_list.append(current.title)
    print(current.title)
    total_articles = 1
    
    # keeps printing as long as there's children
    while current.child is not None:
        current = current.child
        art_list.append(current.title)
        print(current.title)
        total_articles += 1

    return total_articles, art_list

def web_main(article1, article2):
    global start
    global end
    start = Article(article1)
    end = Article(article2)

    asyncio.run(solve(start, end))
    
    tot_articles, art_list = printer(start)
    # print(art_list)
    str_output = " -> ".join(art_list)
    # print(str_output)
    return str_output

