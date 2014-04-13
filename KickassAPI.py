#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple kickass.to API by cyl1ch/FEE1DEAD 
"""
from pyquery import PyQuery
from collections import namedtuple

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

    """
    Class for parsing latest torrents at http://www.kickass.to/new/
    """
    def __init__(self, field=None, order=None):
        self.url = "http://www.kickass.to/new"
        self.tpage = 1
        self.url += "/" + str(self.tpage) + "/"
        if field:
            if field not in fields:
                raise ValueError("Field not recognized")
            if order:
                if order not in orders:
                    raise ValueError("Order not recognized")
            else:
                order = "desc"
            self.url += "?field=" + field + "&sorder=" + order

        pq = PyQuery(url=self.url)
        tds = int(pq("h2").text().split()[-1])
        if tds % 25:
            self.max_page = tds / 25 + 1
        else:
            self.max_page = tds / 25

    def _change_page(self, page):
        """
        Change current page without checking its validity
        """
        size = len(str(self.tpage)) + 1
        self.url = self.url[:-size] + str(page) + '/'
        self.tpage = page

    def next(self):
        """
        Increment page by one
        """
        if self.tpage >= self.max_page:
            raise IndexError("Max page achieved")
        self._change_page(self.tpage + 1)
        return self

    def previous(self):
        """
        Decrement page by one
        """
        if self.tpage <= 1:
            raise IndexError("Page cant be lower than 1")
        self._change_page(self.tpage - 1)
        return self

    def page(self, page_num):
        """
        Change page to argument
        """
        if page_num <= 1 and page_num > self.max_page:
            raise IndexError("Invalid page number")
        self._change_page(page_num)
        return self

    def pages(self, page_from, page_to):
        """
        Yield torrents in range from page_from to page_to
        """
        if not all([page_from < self.max_page,  page_from > 0,
                   page_to <= self.max_page, page_to > page_from]):
            raise IndexError("Invalid page numbers")

        ret = []
        ret.extend(self.page(page_from).list())
        for x in range(page_to - page_from):
            ret.extend(self.next().list())

        for torrent in ret:
            yield torrent

    def all(self):
        """
        Yield torrents from current page to last page
        """
        if(self.tpage == self.max_page):
            return self

        return self.pages(self.tpage, self.max_page)

    def order(self, field, order=None):
        """
        Order by field and optional desc/asc
        """
        return Latest(field=field, order=order)

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
        author = td("a.plain").text()
        verified_author = True if td("img") else False
        category = td("span").find("strong").find("a").eq(0).text()
        verified_torrent = True if td("a.iverify.icon16") else False
        comments = td("a.icomment.icommentjs.icon16").text()
        torrent_link = td("a.cellMainLink").attr("href")
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
        pq = PyQuery(url=self.url)
        torrents = [self._get_torrent(x) for x in self._get_trs(pq)]

        for t in torrents:
            yield t

    def list(self):
        """
        Return list of Torrent namedtuples
        """
        pq = PyQuery(url=self.url)
        torrents = [self._get_torrent(x) for x in self._get_trs(pq)]

        return torrents


class Search(Latest):
    """
    Class for parsing search results
    """
    def __init__(self, query, category=None, field=None, order=None):
        self.url = "http://www.kickass.to/search/"
        self.tpage = 1
        if not query:
            raise ValueError("Query cant be blank")
        self.tquery = query
        self.url += self.tquery
        if category:
            if category not in categories:
                raise ValueError("Category not recognized")
            self.tcategory = category
            self.url = self.url + " category:" + self.tcategory
        else:
            self.tcategory = None
        self.url += "/" + str(self.tpage) + "/"
        if field:
            if field not in fields:
                raise ValueError("Field not recognized")
            if order:
                if order not in orders:
                    raise ValueError("Order not recognized")
            else:
                order = "desc"
            self.url += "?field=" + field + "&sorder=" + order

        pq = PyQuery(url=self.url)
        text = pq("h2").text()
        if "Nothing found" in text:
            raise ValueError("Nothing found for your query")
        self.max_page = int(text.split()[-1]) / 25 + 1

    def category(self, category):
        """
        Change category of current search
        """
        return Search(self.tquery, category=category)

    def order(self, field, order=None):
        """
        Order by field and optional desc/asc
        """
        return Search(self.tquery, category=self.tcategory,
                      field=field, order=order)


def lookup(Torrent):
    """
    Print basic stuff from namedtuple Torrent
    """
    print "%s by %s, size: %s, uploaded %s ago" % (Torrent[0], Torrent[1],
                                                   Torrent[4], Torrent[6])
