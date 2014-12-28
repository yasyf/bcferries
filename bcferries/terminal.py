from abstract import BCFerriesAbstractObject, cacheable, fuzzy
import re, dateutil.parser
from route import BCFerriesRoute

class BCFerriesTerminal(BCFerriesAbstractObject):
  def __init__(self, name, url, api):
    self.name = name
    self.url = url
    self.__api = api

  @cacheable
  def updated_at(self):
    self.__api.set_page(self.url)
    updated = self.__api.find_by_selector('div.conditions > div.white-small-text')[0]
    time = re.match(r'Conditions as at (.*)', updated.text.strip()).group(1)
    return dateutil.parser.parse(time)

  @fuzzy
  @cacheable
  def routes(self):
    self.__api.set_page(self.url)
    divs = self.__api.find_by_selector('div.ferry_name > div.td')
    return {x.text:BCFerriesRoute(self.__api, i) for i,x in enumerate(divs)}
