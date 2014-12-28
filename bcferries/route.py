from abstract import BCFerriesAbstractObject, cacheable
from crossing import BCFerriesCrossing
from scheduled import BCFerriesScheduledCrossing
import re

class BCFerriesRoute(BCFerriesAbstractObject):
  def __init__(self, api, index):
    self.__api = api
    self.name = self.__api.find_by_selector('div.ferry_name > div.td')[index].text
    self.__time_block = self.__api.find_by_selector('div.time_block > div.td > div')[index]
    self.car_waits = int(self.__api.find_by_selector('div.car_waits > div.td > div')[index].text)
    self.oversize_waits = int(self.__api.find_by_selector('div.car_waits > div.td > div')[index + 1].text)
    self.__schedule_url = self.__api.find_by_selector('div.buttons')[index].find('a').get('href')

  def crossings(self):
    rows = self.__time_block.find_all('tr')
    return {x.find('td').text:BCFerriesCrossing(self.name, x, self.__api) for x in rows}

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

