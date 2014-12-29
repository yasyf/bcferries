import requests, functools32, datetime
from bs4 import BeautifulSoup
from urlparse import urlparse

class BCFerriesAPI(object):

  cache_size = 16
  cache_for = datetime.timedelta(minutes=5)

  def __init__(self, api_root):
    self.api_root = api_root
    self.ignore_cache = False
    self.last_cleared = datetime.datetime.now()
    self.set_page(api_root)

  @functools32.lru_cache(cache_size)
  def __get_page(self, url):
    html = requests.get(url).text
    return BeautifulSoup(html)

  def _flush_cache(self):
    self.__get_page.cache_clear()
    self.last_cleared = datetime.datetime.now()

  def get_page(self):
    return self.bs

  def set_page(self, url):
    if 'http' not in url:
      o = urlparse(self.api_root)
      url = "{}://{}{}".format(o.scheme, o.hostname, url)
    if self.ignore_cache:
      self.bs = self.__get_page.__wrapped__(self, url)
    else:
      self.bs = self.__get_page(url)

  def find_by_predicate(self, tag, predicate):
    return self.bs.find_all(tag, predicate)

  def find_by_selector(self, selector):
    return self.bs.select(selector)

def set_cache_size(i):
  BCFerriesAPI.cache_size = i

def set_cache_timeout(timedelta):
  BCFerriesAPI.cache_for = timedelta
