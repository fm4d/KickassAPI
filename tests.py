import KickassAPI
import pytest

BASE_URL = "http://" + KickassAPI.BASE.domain

"""
This submodule uses pytest framework: http://pytest.org
"""
class TestURL:
    """
    Url, LatestUrl, UserUrl, and SearchUrl tests
    """
    def setup_method(self, method):
        self.url = KickassAPI.Url()
        self.url.page = 2
        self.url.max_page = 3

    def test_inc(self):
        self.url.inc_page()
        assert self.url.page == 3

        with pytest.raises(IndexError):
            self.url.inc_page()

    def test_dec(self):
        self.url.dec_page()
        assert self.url.page == 1

        with pytest.raises(IndexError):
            self.url.dec_page()

    def test_set(self):
        self.url.set_page(3)
        assert self.url.page == 3

        self.url.set_page(1)
        assert self.url.page == 1

        with pytest.raises(IndexError):
            self.url.set_page(8)

    def test_latest_build(self):
        latest = KickassAPI.LatestUrl(1, None)
        res = BASE_URL + "/new/1/"
        assert latest.build(update=False) == res

        latest2 = KickassAPI.LatestUrl(1, (KickassAPI.ORDER.AGE,
                                           KickassAPI.ORDER.ASC))
        res2 = BASE_URL + "/new/1/?field=time_add&sorder=asc"
        assert latest2.build(update=False) == res2

    def test_search_build(self):
        search = KickassAPI.SearchUrl("test", 1, None, None)
        res = BASE_URL + "/usearch/test/1/"
        assert search.build(update=False) == res

        search2 = KickassAPI.SearchUrl("test", 1, KickassAPI.CATEGORY.GAMES,
                            (KickassAPI.ORDER.SIZE, KickassAPI.ORDER.DESC))
        res2 = (BASE_URL + "/usearch/test category:games/1/"
               "?field=size&sorder=desc")
        assert search2.build(update=False) == res2

    def test_user_build(self):
        user = KickassAPI.UserUrl("reduxionist", 1, None)
        res = BASE_URL + "/user/reduxionist/uploads/?page=1"
        assert user.build(update=False) == res

        user2 = KickassAPI.UserUrl("reduxionist", 1, (KickassAPI.ORDER.SIZE,
                                                      KickassAPI.ORDER.DESC))
        res2 = (BASE_URL + "/user/reduxionist/uploads/"
               "?page=1&field=size&sorder=desc")
        assert user2.build(update=False) == res2

