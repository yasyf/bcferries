from api import BCFerriesAPI
from terminal import BCFerriesTerminal
from abstract import BCFerriesAbstractObject, cacheable, fuzzy
from urlparse import urlparse

class BCFerries(BCFerriesAbstractObject):

  DEFAULT_API_ROOT = 'http://mobile.bcferries.com/'

  def __init__(self, api_root=DEFAULT_API_ROOT):
    super(BCFerries, self).__init__(self)

    self._api = BCFerriesAPI(api_root)
    self.name = urlparse(api_root).hostname

    self._register_properties(['terminals'])

  def flush_cache(self):
    self._api._flush_cache()

  @fuzzy
  @cacheable
  def terminals(self):
    self._api.set_page(self._api.api_root)
    divs = self._api.find_by_predicate('div', ['terminal_even', 'terminal_odd'])
    links = [x.find('a') for x in divs]
    return {x.text:BCFerriesTerminal(x.text, x.get('href'), self._api) for x in links}

  @cacheable
  def terminal(self, name):
    return self.terminals()[name]
