from abstract import BCFerriesAbstractObject
from capacity import BCFerriesCapacity
import dateutil.parser

class BCFerriesCrossing(BCFerriesAbstractObject):
  def __init__(self, name, row, api):
    super(BCFerriesCrossing, self).__init__(self)

    self.route_name = name
    self._api = api

    time, percent_full = row.find_by_tag('td')
    self.time = dateutil.parser.parse(time.text)
    self.name = "{} at {}".format(name, time.text)
    self.capacity = BCFerriesCapacity(percent_full.find_one('a'))

    self._register_properties(['route_name', 'time', 'name', 'capacity'])
