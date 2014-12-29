from api import BCFerriesAPI
from terminal import BCFerriesTerminal
from abstract import BCFerriesAbstractObject
from decorators import cacheable, fuzzy
from urlparse import urlparse
from geopy.distance import distance
import functools32, os

class BCFerries(BCFerriesAbstractObject):

  DEFAULT_API_ROOT = 'http://mobile.bcferries.com/'
  GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

  def __init__(self, api_root=DEFAULT_API_ROOT, google_maps_api_key=GOOGLE_MAPS_API_KEY):
    super(BCFerries, self).__init__(self)

    self._api = BCFerriesAPI(api_root, self, google_maps_api_key)
    self.name = urlparse(api_root).hostname

    self._register_properties(['terminals'])

  def flush_cache(self):
    self._api._flush_cache()

  @fuzzy
  @cacheable
  def terminals(self):
    page = self._api.get_page(self._api.api_root)
    divs = page.find_by_predicate('div', ['terminal_even', 'terminal_odd'])
    links = [x.find_one('a') for x in divs]
    return {x.text:BCFerriesTerminal(x.text, x.get('href'), self._api) for x in links}

  @cacheable
  def terminal(self, name):
    return self.terminals()[name]

  @functools32.lru_cache(128)
  def nearest_terminal(self, *args):
    loc = self._api.geocode(*args)
    return min(self.terminals().values(), key=lambda x: distance(loc[1], x.location()[1]))
