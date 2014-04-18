KickassAPI
==========
This is unofficial Python API for kickass.to

Usage
=====
There are two objects - ``Search`` for searching and Latest for ``kickass.to/new/``Torrents are parsed into `namedtuples` called Torrent and there is a function ``lookup()``if you want to simply print name, author, size and age of namedtuple Torrent.

Search for first page of "Game of thrones" and print it with ``lookup()``:

```python
for t in Search("Game of thrones"):
    lookup(t)
```

``next()`` and ``previous()`` allows traversing throught result pages:

```python
for t in Search("Game of thrones").next():
    lookup(t)
```
    
You can choose category using ``category("category")`` and order using ``order("field", "order")``, valid orders are "asc" -> ascending and "desc" -> descending. ``order("field")`` will use "desc" as default value


```python
s = Search("Game of thrones")
for t in s.order("time_add","asc"):
    lookup(t)
```

```python
s = Search("Game of thrones")
for t in s.category("tv"):
    lookup(t)
```

``all()`` returns all torrents starting on current page. 

```python
Search("Game of thrones").all()
```

``pages(from,to)`` returns all torrents in interval from - to.

```python
Search("Game of thrones").pages(3,6)
```

Feel free to chain commands as you wish, only rule is to use all() or pages() as  
last, because it directly returns Torrents. For example:

```python
for t in (Search("Game of thrones").category("tv").order("time_add","asc")
          .page(84).next().previous().all()):
    lookup(t)
```

You can also pass parameters directly:

```python
Search("Game of thrones",category="games",field="size",order="desc")
```

``Latest`` works exactly like ``Search``, but you can't use categories or pass search query.

```python
for t in Latest().page(5):
    lookup(t)
```
