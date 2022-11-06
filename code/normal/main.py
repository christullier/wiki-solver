import sys
from time import time

from Article import *
from Search import *

# left node is starting and right is ending
def solve(left, right):
    # get links here because the for loop won't work without them
    left.forwardlinks()
    right.backlinks()

    if start.title in end.links or end.title in start.links: 
        left(right)
        right(left)
        return

    # check if lists match up
    # check current left node against the end node and its parents
    r = end
    while r != None:
        for item in left.links:
            if item in r.links:
                new = Article(item)
                left(new)
                new(r)
                return
        r = r.parent
    
    # check current right node against the start node and it's children
    l = start
    while l != None:
        for item in right.links:
            if item in l.links:
                new = Article(item)
                l(new)
                new(right)
                return
        l = l.parent

    left.get_views_dict()
    right.get_views_dict()

    left.child = Article(left.best_link())
    right.parent = Article(right.best_link())

    left(left.child) # callable that links parent(child)
    right.parent(right) # right is the child in this case because we're using backlinks
    
    sys.stdout.write("\033[F")

    print()
    sys.stdout.write("\033[K")
    sys.stdout.write(f"{left.child.title} <---> {right.parent.title}")
    sys.stdout.flush()    
    solve(left.child, right.parent)


# prints list of articles with the game's solution (you gotta solve first solving)
def printer(start_article):
    print("\n")
    current = start_article

    print(current.title)
    total_articles = 1

    # keeps printing as long as there's children
    while current.child is not None and current.child is not start_article:
        current = current.child
        print(current.title)
        total_articles += 1

    return total_articles        

if __name__ == "__main__":
    name1 = "Avengers (comics)" # starting article
    name2 = "The Room" # finish article
    
    if len(sys.argv) == 2:
        if str(sys.argv[1]) == "-h":
            exit("Usage: main.py [start article] [end article]")
    
    elif len(sys.argv) == 3:
        cmd1 = str(sys.argv[1])
        cmd2 = str(sys.argv[2])
    else:
        cmd1 = input('starting link: ')
        s1 = Search(cmd1)
        if not (s1.results[0].lower() == cmd1.lower()):
            for i in range(len(s1.results)):
                print(f"\t{i} {s1.results[i]}")
            choice = int(input("Type a number to choose one: "))
            cmd1 = s1.results[choice]
        cmd2 = input('ending link: ')
        s2 = Search(cmd2)
        if not (s2.results[0].lower() == cmd2.lower()):
            for i in range(len(s2.results)):
                print(f"\t{i} {s2.results[i]}")
            choice = int(input("Type a number to choose one: "))
            cmd2 = s2.results[choice]
    
    # check here if the article is a valid one - so the user doesn't have to find out later
    # perhaps search for an article and return options if it doesn't exist
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
    solve(start, end)
    tf = time()

    tot_articles = printer(start)
    
    tot_time = round(tf-ti, 2)
    print()
    print(f"{tot_time}s total runtime")
    print(f"{tot_articles} total articles")
    print(f"{round(tot_time/tot_articles, 2)}s per article")
