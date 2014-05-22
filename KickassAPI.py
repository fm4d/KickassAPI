#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Version: 2.7
# Author: FEE1DE4D


# TODO
# JSON export

from pyquery import PyQuery
from collections import namedtuple
import threading

# possible categories
categories = ("movies", "tv", "music", "books", "games", "applications", "xxx")
# possible fields
fields = ("size", "file_count", "time_add", "seeders", "leechers")
# possible orders
orders = ("asc", "desc")

# Namedtuple for single torrent
Torrent = namedtuple("Torrent", ["name", "author", "verified_author",
                                 "category", "size", "files", "age", "seed",
                                 "leech", "verified_torrent", "comments",
                                 "torrent_link", "magnet_link", "download_link"
                                 ])


class Latest(object):

    def __init__(self, field=None, order=None, page=None):
        self._base_url = "http://www.kickass.to/new"
        if page:
            self._page = page
        else:
            self._page = 1
        if field:
            if field not in fields:
                raise ValueError("Field not recognized")
            self._field = field
            if order:
                if order not in orders:
                    raise ValueError("Order not recognized")
                self._order = order
            self._order = "desc"
        else:
            self._field = None
            self._order = None

        pq = PyQuery(url=self._get_url())
        tds = int(pq("h2").text().split()[-1])
        if tds % 25:
            self._max_page = tds / 25 + 1
        else:
            self._max_page = tds / 25

    def _get_url(self):
        """
        Assemble and return url
        """
        url = self._base_url + '/' + str(self._page) + '/'
        if self._field:
            url = url + "?field=" + self._field + "&sorder=" + self._order
        return url

    def _change_page(self, page):
        """
        Change current page without checking its validity
        """
        self._page = page
        return self.__class__(self._field, self._order, self._page)

    def next(self):
        """
        Increment page by one
        """
        if self._page >= self._max_page:
            raise IndexError("Max page achieved")
        return self._change_page(self._page + 1)

    def previous(self):
        """
        Decrement page by one
        """
        if self._page <= 1:
            raise IndexError("Page cant be lower than 1")
        return self._change_page(self._page - 1)

    def page(self, page_num):
        """
        Change page to page_num
        """
        if page_num <= 1 and page_num > self._max_page:
            raise IndexError("Invalid page number")
        return self._change_page(page_num)

    def pages(self, page_from, page_to):
        """
        Yield torrents in range from page_from to page_to
        """
        if not all([page_from < self._max_page,  page_from > 0,
                   page_to <= self._max_page, page_to > page_from]):
            raise IndexError("Invalid page numbers")

        size = (page_to + 1) - page_from
        threads = ret = []
        page_list = [n for n in range(page_from, page_to+1)]

        locks = [threading.Lock() for i in range(size)]

        for pos, value in enumerate(locks):
            if pos > 0:
                value.acquire()

        def t_function(pos):
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
        if(self._page == self._max_page):
            return self

        return self.pages(self._page, self._max_page)

    def order(self, field, order=None):
        """
        Return new Lates with field and order set by arguments
        """
        return Latest(field=field, order=order, page=self._page)

    def __iter__(self):
        return self.items()

    def _get_trs(self, pq):
        """
        Return all rows on page
        """
        rows = pq("table.data").find("tr")
        return [rows.eq(x) for x in range(rows.size())][1:]

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

        return Torrent(name, author, verified_author, category, size, files,
                       age, seed, leech, verified_torrent, comments,
                       torrent_link, magnet_link, download_link)

    def items(self):
        """
        Parse url and yield namedtuple Torrent for every torrent on page
        """
        pq = PyQuery(url=self._get_url())
        torrents = [self._get_torrent(x) for x in self._get_trs(pq)]

        for t in torrents:
            yield t

    def list(self):
        """
        Return list of Torrent namedtuples
        """
        pq = PyQuery(url=self._get_url())
        torrents = [self._get_torrent(x) for x in self._get_trs(pq)]

        return torrents


class Search(Latest):

    def __init__(self, query, category=None, field=None,
                 order=None, page=None):
        self._base_url = "http://www.kickass.to/search"
        if page:
            self._page = page
        else:
            self._page = 1
        if not query:
            raise ValueError("Query cant be blank")
        self._query = query
        if category:
            if category not in categories:
                raise ValueError("Category not recognized")
            self._category = category
        else:
            self._category = None
        if field:
            if field not in fields:
                raise ValueError("Field not recognized")
            self._field = field
            if order:
                if order not in orders:
                    raise ValueError("Order not recognized")
                self._order = order
            else:
                self._order = "desc"
        else:
            self._field = None
            self._order = None

        pq = PyQuery(url=self._get_url())
        tds = int(pq("h2").text().split()[-1])
        if tds % 25:
            self._max_page = tds / 25 + 1
        else:
            self._max_page = tds / 25

    def _get_url(self):
        """
        Assemble and return url
        """
        base_url = self._base_url + '/' + self._query
        if self._category:
            base_url += " category:" + self._category
        url = base_url + '/' + str(self._page) + '/'
        if self._field:
            url = url + "?field=" + self._field + "&sorder=" + self._order
        return url

    def _change_page(self, page):
        """
        Change current page without checking its validity
        """
        self._page = page
        return self.__class__(self._query, self._category,
                              self._field, self._order, self._page)

    def category(self, category):
        """
        Change category of current search
        """
        return Search(self._query, category=category, field=self._field,
                      order=self._order, page=self._page)

    def order(self, field, order=None):
        """
        Order by field and optional desc/asc
        """
        return Search(self._query, category=self._category, field=field,
                      order=order, page=self._page)


def lookup(Torrent):
    """
    Print basic stuff from namedtuple Torrent
    """
    print "%s by %s, size: %s, uploaded %s ago" % (Torrent[0], Torrent[1],
                                                   Torrent[4], Torrent[6])
