KickassAPI
==========
This is unofficial Python API for kickass.to

Usage
=====
There are two objects - ``Search`` for searching and Latest for ``kickass.to/new/``
Torrents are parsed into `namedtuples` called Torrent and there is function ``lookup()``
to simply print name, author, size and age of torrent.

Print first 25 torrents matching "Game of thrones":

```python
for t in Search("Game of thrones"):
    lookup(t)
```

Print more (25-50) results matching of "Game of thrones":

```python
for t in Search("Game of thrones").next():
    lookup(t)
```

Use ``previous()`` to get previous page and ``page()`` to jump to any page.

Print 1-100 of "Game of thrones":

```python
for t in Search("Game of thrones").pages(1,4):
    lookup(t)
```
    
You can choose category using ``category("category")`` and order using 
``order("field", "order")``, for example:

```python
s = Search("Game of thrones")
for t in s.order("time_add","asc")
    lookup(t)
```

If you dont give to the ``order()`` the second argument, default value will be
``"desc"``.

``all()`` returns all torrents beggining from current page, for example:

```python
Search("Game of thrones").page(5).all()
```

This will return all torrents, beggining at page 5.

You can also pass adition parameters to ``Search``:

```python
Search("Game of thrones",category="games",field="size",order="desc")
```

Don't use the ``category()`` or ``order()`` modificators after you've used 
``pages()``.

``Latest`` works exactly like ``Search``, but you can't use categories.
