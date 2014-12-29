from abstract import BCFerriesAbstractObject, cacheable, fuzzy
import re, dateutil.parser
from route import BCFerriesRoute

class BCFerriesTerminal(BCFerriesAbstractObject):
  def __init__(self, name, url, api):
    super(BCFerriesTerminal, self).__init__(self)

    self.name = name
    self.__url = url
    self._api = api

    self._register_properties(['updated_at', 'routes'])

  @cacheable
  def updated_at(self):
    self._api.set_page(self.__url)
    updated = self._api.find_by_selector('div.conditions > div.white-small-text')[0]
    time = re.match(r'Conditions as at (.*)', updated.text.strip()).group(1)
    return dateutil.parser.parse(time)

  @fuzzy
  @cacheable
  def routes(self):
    self._api.set_page(self.__url)
    divs = self._api.find_by_selector('div.ferry_name > div.td')
    return {x.text:BCFerriesRoute(self._api, i) for i,x in enumerate(divs)}

  @cacheable
  def route(self, name):
    return self.routes()[name]
