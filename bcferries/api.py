import requests, functools32
from bs4 import BeautifulSoup
from urlparse import urlparse

class BCFerriesAPI(object):
  def __init__(self, api_root):
    self.api_root = api_root
    self.set_page(api_root)

  @functools32.lru_cache()
  def __get_page(self, url):
    html = requests.get(url).text
    return BeautifulSoup(html)

  def _flush_cache(self):
    self.__get_page.cache_clear()

  def get_page(self):
    return self.bs

  def set_page(self, url):
    if 'http' not in url:
      o = urlparse(self.api_root)
      url = "{}://{}{}".format(o.scheme, o.hostname, url)
    self.bs = self.__get_page(url)

  def find_by_predicate(self, tag, predicate):
    return self.bs.find_all(tag, predicate)

  def find_by_selector(self, selector):
    return self.bs.select(selector)
