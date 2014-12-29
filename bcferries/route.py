from abstract import BCFerriesAbstractObject
from decorators import cacheable, fuzzy
from crossing import BCFerriesCrossing
from scheduled import BCFerriesScheduledCrossing
from helpers import to_int
from geopy.distance import distance
import re, datetime

class BCFerriesRoute(BCFerriesAbstractObject):
  def __init__(self, api, page, index):
    super(BCFerriesRoute, self).__init__(self)

    self._api = api
    self.name = page.find_by_selector('div.ferry_name > div.td')[index].text
    self.__time_block = page.find_by_selector('div.time_block > div.td > div')[index]
    self.car_waits = to_int(page.find_by_selector('div.car_waits > div.td > div')[index].text)
    self.oversize_waits = to_int(page.find_by_selector('div.car_waits > div.td > div')[index + 1].text)
    self.__schedule_url = page.find_by_selector('div.buttons')[index].find_one('a').get('href')

    from_, to = self.name.split(' to ')
    self.from_ = api.bc.terminals().get(from_)
    self.to = api.bc.terminals().get(to)

    self._register_properties(['car_waits', 'oversize_waits', 'crossings', 'schedule', 'distance', 'from_', 'to'])

  def distance(self):
    return distance(self.from_.location()[1], self.to.location()[1])

  @fuzzy
  @cacheable
  def crossings(self):
    rows = self.__time_block.find_by_tag('tr')
    return {x.find_one('td').text:BCFerriesCrossing(self.name, x, self._api) for x in rows}

  @cacheable
  def crossing(self, name):
    return self.crossings()[name]

  @cacheable
  def next_crossing(self):
    now = datetime.datetime.now()
    crossings = self.crossings()
    crossings = filter(lambda x: x.time > now, crossings.values())
    if crossings:
      return min(crossings, key=lambda x: x.time - now)

  @fuzzy
  @cacheable
  def schedule(self):
    page = self._api.get_page(self.__schedule_url)
    sailing_time = page.find_by_selector('div.sched_sailingtime > b')[0].text
    sailing_time = re.match(r'SAILING TIME: (.*)', sailing_time.strip()).group(1)
    rows = page.find_by_selector('table.scheduleTable > tbody > tr')
    scheduled = {}
    i = 0
    while i < len(rows):
      name = rows[i].find_one('td').text.strip()
      time_row = [x.text for x in rows[i + 1].find_by_tag('td')]
      scheduled[time_row[0]] = BCFerriesScheduledCrossing(name, sailing_time, time_row)
      i += 2
    return scheduled

  @cacheable
  def scheduled(self, name):
    return self.schedule()[name]
