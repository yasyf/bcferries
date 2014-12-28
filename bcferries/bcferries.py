from api import BCFerriesAPI
from terminal import BCFerriesTerminal
from abstract import cacheable, fuzzy

class BCFerries(object):

  DEFAULT_API_ROOT = 'http://mobile.bcferries.com/'

  def __init__(self, api_root=DEFAULT_API_ROOT):
    self.__api = BCFerriesAPI(api_root)

  @cacheable
  def terminals(self):
    self.__api.set_page(self.__api.api_root)
    divs = self.__api.find_by_predicate('div', ['terminal_even', 'terminal_odd'])
    links = [x.find('a') for x in divs]
    return {x.text:BCFerriesTerminal(x.text, x.get('href'), self.__api) for x in links}

  @fuzzy
  @cacheable
  def terminal(self, name):
    return self.terminals()[name]
