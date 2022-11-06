import asyncio
import sys
from time import time

from Article import *


# left node is starting and right is ending
async def solve(left, right):
    # get links here because the for loop won't work without them
    await asyncio.gather(
        left.forwardlinks(),
        right.backlinks())

    if left.title in right.links or right.title in left.links: 
        left(right)
        right(left)
        return
    # check current left node against the end node and its parents
    right_node = end
    while right_node != None:
        for item in left.links:
            if item in right_node.links:
                new = Article(item)
                left(new)
                new(right_node)
                return
        right_node = right_node.parent
    
    # check current right node against the start node and it's children
    left_node = start
    while left_node != None:
        for item in right.links:
            if item in left_node.links:
                new = Article(item)
                left_node(new)
                new(right)
                return
        left_node = left_node.parent

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
"""  

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
    
    global start 
    global end
    start = Article(name1)
    end = Article(name2)

    print("Searching", end="")

    ti = time()
    asyncio.run(solve(start, end))
    tf = time()

    tot_articles, art_list = printer(start)
    
    tot_time = round(tf-ti, 2)
    print()
    print(f"{tot_time}s total runtime")
    print(f"{tot_articles} total articles")
    print(f"{round(tot_time/tot_articles, 2)}s per article")
"""


async def bot_main(article1, article2):
    global start
    global end
    start = Article(article1)
    end = Article(article2)

    (
    await solve(start, end)
    )
    tot_articles, art_list = printer(start)
    # print(art_list)
    str_output = " -> ".join(art_list)
    # print(str_output)
    return str_output

# bot_main("Avengers_(comics)", "The_Room")
