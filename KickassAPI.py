#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Version: 2.7
# Author: FEE1DE4D

"""
This is an unofficial python API for kickass.to partially
inspired by https://github.com/karan/TPB.karan

by FEE1DE4D (fee1de4d@gmail.com)
under GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
"""


# IMPORTS
from pyquery import PyQuery
import threading
import sys
from collections import namedtuple


# CONSTANTS
class BASE(object):
    SEARCH = "http://www.kickass.to/usearch/"
    LATEST = "http://www.kickass.to/new/"

class CATEGORY(object):
    MOVIES = "movies"
    TV = "tv"
    MUSIC = "music"
    BOOKS = "books"
    GAMES = "games"
    APPLICATIONS = "applications"
    XXX = "xxx"

class ORDER(object):
    SIZE = "size"
    FILES_COUNT = "files_count"
    AGE = "time_add"
    SEED = "seeders"
    LEECH = "leechers"
    ASC = "asc"
    DESC = "desc"


class Torrent(namedtuple("Torrent", ["name", "author", "verified_author",
                                     "category", "size", "files", "age",
                                     "seed", "leech", "verified_torrent",
                                     "comments", "torrent_link",
                                     "magnet_link", "download_link"
                                    ])):
    """
    Namedtuple that holds information about single torrent
    Subclassed to add "lookup" function
    """
    def lookup(self):
        """
        Prints name, author, size and age
        """
        print "%s by %s, size: %s, uploaded %s ago" % (self.name, self.author,
                                                       self.size, self.age)


class Url(object):
    """
    Abstract class that provides functionality for holding and
    building url. Subclass must overwrite constructor and build method.
    """
    def inc_page(self):
        if self.page >= self.max_page:
            raise IndexError("Max page achieved")
        self.page += 1

    def dec_page(self):
        if self.page <= 1:
            raise IndexError("Min page achieved")
        self.page -= 1

    def set_page(self, page):
        if page < 1 or page > self.max_page:
            raise IndexError("Invalid page number")
        self.page = page

    def _get_max_page(self, url):
        """
        Open url and return ammount of pages
        """
        pq = PyQuery(url)
        try:
            tds = int(pq("h2").text().split()[-1])
            if tds % 25:
                return tds / 25 + 1
            return tds / 25
        except ValueError:
            sys.stderr.write("No results found!\n")
            sys.exit()

    def build(self):
        """
        Build and return url. Must be overwritten in subclass.
        """
        raise NotImplementedError("This method must be overwritten")


class LatestUrl(Url):

    def __init__(self, page, order, ):
        self.base = BASE.LATEST
        self.page = page
        self.order = order
        self.max_page = None
        self.build()

    def build(self, update=True):
        """
        Build and return url. Also updates max_page.
        """
        ret = "".join((self.base, str(self.page), "/"))

        if self.order:
            ret += "".join(("?field=", self.order[0],"&sorder=",self.order[1]))

        if update:
            self.max_page = self._get_max_page(ret)

        return ret



class SearchUrl(Url):

    def __init__(self, query, page, category, order):
        self.base = BASE.SEARCH
        self.query = query
        self.page = page
        self.category = category
        self.order = order
        self.max_page = None
        self.build()

    def build(self, update=True):
        """
        Build and return url. Also update max_page.
        """
        ret = self.base + self.query
        page = "".join(("/", str(self.page), "/"))

        if self.category:
            category = " category:" + self.category
        else:
            category = ""

        if self.order:
            order = "".join(("?field=",self.order[0],"&sorder=",self.order[1]))
        else:
            order = ""

        ret = "".join((self.base, self.query, category, page, order))

        if update:
            self.max_page = self._get_max_page(ret)
        return ret



class Results(object):
    """
    Abstract class that contains basic functionality for parsing page
    containing torrents, generating namedtuples and iterating over them.
    """
    # Get rid of linting errors
    url = None

    def __iter__(self):
        return self._items()

    def _items(self):
        """
        Parse url and yield namedtuple Torrent for every torrent on page
        """
        torrents = map(self._get_torrent, self._get_rows())

        for t in torrents:
            yield t

    def list(self):
        """
        Return list of Torrent namedtuples
        """
        torrents = map(self._get_torrent, self._get_rows())

        return torrents

    def _get_torrent(self, row):
        """
        Parse row into namedtuple
        """
        td = row("td")
        name = td("a.cellMainLink").text()
        name = name.replace(" . ", ".").replace(" .", ".")
        author = td("a.plain").text()
        verified_author = True if td("img") else False
        category = td("span").find("strong").find("a").eq(0).text()
        verified_torrent = True if td("a.iverify.icon16") else False
        comments = td("a.icomment.icommentjs.icon16").text()
        torrent_link = "http://www.kickass.to"
        torrent_link += td("a.cellMainLink").attr("href")
        magnet_link = td("a.imagnet.icon16").attr("href")
        download_link = td("a.idownload.icon16").eq(1).attr("href")

        td_centers = row("td.center")
        size = td_centers.eq(0).text()
        files = td_centers.eq(1).text()
        age = " ".join(td_centers.eq(2).text().split())
        seed = td_centers.eq(3).text()
        leech = td_centers.eq(4).text()

        return Torrent(name, author, verified_author, category, size,
                       files, age, seed, leech, verified_torrent, comments,
                       torrent_link, magnet_link, download_link)

    def _get_rows(self):
        """
        Return all rows on page
        """
        #TODO - caching
        pq = PyQuery(url=self.url.build())
        rows = pq("table.data").find("tr")
        return map(rows.eq, range(rows.size()))[1:]

    def next(self):
        """
        Increment page by one and return self
        """
        self.url.inc_page()
        return self

    def previous(self):
        """
        Decrement page by one and return self
        """
        self.url.dec_page()
        return self

    def page(self, page):
        """
        Change page to page_num
        """
        self.url.set_page(page)
        return self

    def pages(self, page_from, page_to):
        """
        Yield torrents in range from page_from to page_to
        """
        if not all([page_from < self.url.max_page, page_from > 0,
                    page_to <= self.url.max_page, page_to > page_from]):
            raise IndexError("Invalid page numbers")

        size = (page_to + 1) - page_from
        threads = ret = []
        page_list = range(page_from, page_to+1)

        locks = [threading.Lock() for i in range(size)]

        #for pos, value in enumerate(locks):
        #    if pos > 0:
        #       value.acquire()


        for lock in locks[1:]:
            lock.acquire()

        def t_function(pos):
            """
            Thread function that fetch page for list of torrents
            """
            res = self.page(page_list[pos]).list()
            locks[pos].acquire()
            ret.extend(res)
            if pos != size-1:
                locks[pos+1].release()

        threads = [threading.Thread(target=t_function, args=(i,))
                   for i in range(size)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        for torrent in ret:
            yield torrent

    def all(self):
        """
        Yield torrents in range from current page to last page
        """
        return self.pages(self.url.page, self.url.max_page)

    def order(self, field, order=None):
        """
        Set field and order set by arguments
        """
        if not order:
            order = ORDER.DESC
        self.url.order = (field, order)
        self.url.set_page(1)
        return self



class Latest(Results):
    """
    Results subclass that represents http://kickass.to/new/
    """
    def __init__(self, page=1, order=None):
        self.url = LatestUrl(page, order)



class Search(Results):
    """
    Results subclass that represents http://kickass.to/usearch/
    """
    def __init__(self, query, page=1, category=None, order=None):
        self.url = SearchUrl(query, page, category, order)

    def category(self, category):
        """
        Change category of current search and return self
        """
        self.url.category = category
        self.url.set_page(1)
        return self
