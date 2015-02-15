KickassAPI
==========
This is an unofficial python API for kickass.to partially inspired by https://github.com/karan/TPB

Installation
-----------

```
pip install KickassAPI
```

Usage
-----

```Search``` represents ```http://kickass.to/usearch/```, ```Latest``` ```http://kickass.to/new/```, and ```User``` ```http://kickass.to/user/username/uploads/```

```python
from KickassAPI import Search, Latest, User, CATEGORY, ORDER

#Print the basic info about first 25 results of "Game of thrones" search
for t in Search("Game of thrones"):
    t.lookup()

#Do the same with second page
for t in Search("Game of thrones").next():
    t.lookup()

#Or
for t in Search("Gameof thrones").page(2):
    t.lookup()

#Order results by age
Search("Game of thrones").order(ORDER.AGE)

#Default order is descending, you can specify ascending order:
Search("Game of thrones").order(ORDER.AGE, ORDER.ASC)

#Specify category
Search("Game of thrones").category(CATEGORY.MOVIES)

#Feel free to chain these, but remember that order or category resets page to 1
Search("Game of thrones").category(CATEGORY.GAMES).order(ORDER.FILES_COUNT).next()

#Latest has the same behaviour as Search but lacks the ```category()``` method and has no query string
for t in Latest().order(ORDER.SEED):
    t.lookup()

#User also has the same behaviour as Search, and also lacks the ```category()``` method, but takes a username in place of a query string
for t in User('reduxionist'):
    t.lookup()

#Page, order and category can be also specified in constructor
Search("Game of thrones", category=CATEGORY.GAMES, order=ORDER.AGE, page=5)

#Get results from multiple pages
for t in Latest().order(ORDER.AGE).pages(3,6):
    t.lookup()

#Get results from all pages starting with the actual page
for t in Latest().all():
    t.lookup()

#Get list of torrent objects instead of iterator
Latest().list()

#pages(), all() and list() can't be followed by any other method!

```
