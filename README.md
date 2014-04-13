KickassAPI
==========

This is unofficial Python API for kickass.to

Usage
=====

There are two objects - Search for searching and Latest for kickass.to/new/  
Torrents are parsed into namedtuples called Torrent and there is function lookup()  
to simply print name, author, size and age of torrent.

Printing first 25 torrents of "Game of thrones"
```python
for t in Search("Game of thrones"):
    lookup(t)
```
Printing 25-50 of "Game of thrones"
```python
for t in Search("Game of thrones").next():
    lookup(t)
```
Use previous() to get previous page and page() for jump to any page.

Printing 1-100 of "Game of thrones"
```python
for t in Search("Game of thrones").pages(1,4):
    lookup(t)
```
    
You can use category("category") and order("field","order"), for example:
```python
s = Search("Game of thrones")
for t in s.order("time_add","asc")
    lookup(t)
```
If you dont give order() second argument, default value will be "desc"

all() returns all torrents starting from current page,for example:
```python
Search("Game of thrones").page(5).all()
```
return all torrents starting on page 5.
You can pass adition parameters to Search:
```python
Search("Game of thrones",category="games",field="size",order="desc")
```

Object Latest works exactly as Search, but you cant use categories.
