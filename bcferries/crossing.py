from abstract import BCFerriesAbstractObject
from capacity import BCFerriesCapacity
import dateutil.parser

class BCFerriesCrossing(BCFerriesAbstractObject):
  def __init__(self, name, row, api):
    self.route_name = name
    self.__api = api

    time, percent_full = row.find_all('td')
    self.time = dateutil.parser.parse(time.text)
    self.name = "{} at {}".format(name, time.text)
    self.capacity = BCFerriesCapacity(percent_full.find('a'))
