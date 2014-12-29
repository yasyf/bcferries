from abstract import BCFerriesAbstractObject, cacheable, fuzzy
from crossing import BCFerriesCrossing
from scheduled import BCFerriesScheduledCrossing
import re, datetime

class BCFerriesRoute(BCFerriesAbstractObject):
  def __init__(self, api, index):
    super(BCFerriesRoute, self).__init__(self)

    self._api = api
    self.name = self._api.find_by_selector('div.ferry_name > div.td')[index].text
    self.__time_block = self._api.find_by_selector('div.time_block > div.td > div')[index]
    self.car_waits = int(self._api.find_by_selector('div.car_waits > div.td > div')[index].text)
    self.oversize_waits = int(self._api.find_by_selector('div.car_waits > div.td > div')[index + 1].text)
    self.__schedule_url = self._api.find_by_selector('div.buttons')[index].find('a').get('href')

    self._register_properties(['car_waits', 'oversize_waits', 'crossings', 'schedule'])

  @fuzzy
  @cacheable
  def crossings(self):
    rows = self.__time_block.find_all('tr')
    return {x.find('td').text:BCFerriesCrossing(self.name, x, self._api) for x in rows}

  def crossing(self, name):
    return self.crossings()[name]

  def next_crossing(self):
    crossings = self.crossings()
    if crossings:
      return min(crossings.values(), key=lambda x: x.time - datetime.datetime.now())

  @fuzzy
  @cacheable
  def schedule(self):
    self._api.set_page(self.__schedule_url)
    sailing_time = self._api.find_by_selector('div.sched_sailingtime > b')[0].text
    sailing_time = re.match(r'SAILING TIME: (.*)', sailing_time.strip()).group(1)
    rows = self._api.find_by_selector('table.scheduleTable > tbody > tr')
    scheduled = {}
    i = 0
    while i < len(rows):
      name = rows[i].find('td').text.strip()
      time_row = [x.text for x in rows[i + 1].find_all('td')]
      scheduled[time_row[0]] = BCFerriesScheduledCrossing(name, sailing_time, time_row)
      i += 2
    return scheduled

  @cacheable
  def scheduled(self, name):
    return self.schedule()[name]
