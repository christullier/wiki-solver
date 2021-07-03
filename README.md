# Wiki-Solver
## What does it do?
1. Takes two (usually random) wikipedia articles as input
2. Finds a path between them, using only wiki links starting on those pages
3. Prints the path between the two articles

## How to run
* run `pip install httpx`
* run `main.py`
* type in wikipedia links
    * they can be either a wiki link or the title of an article
    * quotes are necessary for command line args if the title has spaces

## Examples:
### Normal:
```
> python main.py
starting link: https://en.wikipedia.org/wiki/Avengers_(comics)
ending link: The Room
Searching...

Avengers_(comics)
Captain America: The First Avenger
Chris Evans (actor)
James Franco
The Room
```

### Command line args:
```
> python main.py "Elon Musk" Muskrat
Searching...

Elon Musk
Mars Society
California
Utah
Muskrat
```

## Da Rules:
* https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game

Made using Python 3.9.5
