import requests, functools32, datetime
from bs4 import BeautifulSoup
from urlparse import urlparse
from geopy.geocoders import GoogleV3

class BCFerriesAPI(object):

  cache_size = 16
  cache_for = datetime.timedelta(minutes=5)

  def __init__(self, api_root, bc, google_maps_api_key=None):
    self.api_root = api_root
    self.bc = bc
    self.ignore_cache = False
    self.last_cleared = datetime.datetime.now()
    self.g = GoogleV3(domain='maps.google.ca', api_key=google_maps_api_key)

  @functools32.lru_cache(cache_size)
  def __get_page(self, url):
    html = requests.get(url).text
    return BeautifulSoup(html)

  @functools32.lru_cache(128)
  def geocode(self, *args, **kwargs):
    return self.g.geocode(*args, **kwargs)

  @functools32.lru_cache(128)
  def reverse(self, *args, **kwargs):
    return self.g.reverse(*args, **kwargs)

  def _flush_cache(self):
    self.__get_page.cache_clear()
    self.last_cleared = datetime.datetime.now()

  def get_page(self, url):
    if 'http' not in url:
      o = urlparse(self.api_root)
      url = "{}://{}{}".format(o.scheme, o.hostname, url)
    if self.ignore_cache:
      bs = self.__get_page.__wrapped__(self, url)
    else:
      bs = self.__get_page(url)
    return BCFerriesAPIPage(bs)

class BCFerriesAPIPage(object):
  def __init__(self, bs):
    self.bs = bs

  @property
  def text(self):
    return self.bs.text

  def get(self, prop):
    return self.bs.get(prop)

  def find_one(self, tag):
    return self.bs.find(tag)

  def find_by_tag(self, tag):
    return self.find_by_predicate(tag, None)

  def find_by_predicate(self, tag, predicate):
    return [BCFerriesAPIPage(x) for x in self.bs.find_all(tag, predicate)]

  def find_by_selector(self, selector):
    return [BCFerriesAPIPage(x) for x in self.bs.select(selector)]

def set_cache_size(i):
  BCFerriesAPI.cache_size = i

def set_cache_timeout(timedelta):
  BCFerriesAPI.cache_for = timedelta
