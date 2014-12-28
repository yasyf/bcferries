from abstract import BCFerriesAbstractObject, cacheable, fuzzy
from crossing import BCFerriesCrossing
from scheduled import BCFerriesScheduledCrossing
import re, datetime

class BCFerriesRoute(BCFerriesAbstractObject):
  def __init__(self, api, index):
    super(BCFerriesRoute, self).__init__(self)

    self.__api = api
    self.name = self.__api.find_by_selector('div.ferry_name > div.td')[index].text
    self.__time_block = self.__api.find_by_selector('div.time_block > div.td > div')[index]
    self.car_waits = int(self.__api.find_by_selector('div.car_waits > div.td > div')[index].text)
    self.oversize_waits = int(self.__api.find_by_selector('div.car_waits > div.td > div')[index + 1].text)
    self.__schedule_url = self.__api.find_by_selector('div.buttons')[index].find('a').get('href')

    self._register_properties(['car_waits', 'oversize_waits', 'crossings', 'schedule'])

  @fuzzy
  def crossings(self):
    rows = self.__time_block.find_all('tr')
    return {x.find('td').text:BCFerriesCrossing(self.name, x, self.__api) for x in rows}

  def next_crossing(self):
    crossings = self.crossings()
    if crossings:
      return min(crossings.values(), key=lambda x: x.time - datetime.datetime.now())

  @fuzzy
  @cacheable
  def schedule(self):
    self.__api.set_page(self.__schedule_url)
    sailing_time = self.__api.find_by_selector('div.sched_sailingtime > b')[0].text
    sailing_time = re.match(r'SAILING TIME: (.*)', sailing_time.strip()).group(1)
    rows = self.__api.find_by_selector('table.scheduleTable > tbody > tr')
    scheduled = {}
    i = 0
    while i < len(rows):
      name = rows[i].find('td').text.strip()
      time_row = [x.text for x in rows[i + 1].find_all('td')]
      scheduled[time_row[0]] = BCFerriesScheduledCrossing(name, sailing_time, time_row)
      i += 2
    return scheduled

