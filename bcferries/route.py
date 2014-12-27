from abstract import BCFerriesAbstractObject
from crossing import BCFerriesCrossing

class BCFerriesRoute(BCFerriesAbstractObject):
  def __init__(self, api, index):
    self.__api = api
    self.name = self.__api.find_by_selector('div.ferry_name > div.td')[index].text
    self.__time_block = self.__api.find_by_selector('div.time_block > div.td > div')[index]
    self.car_waits = int(self.__api.find_by_selector('div.car_waits > div.td > div')[index].text)
    self.oversize_waits = int(self.__api.find_by_selector('div.car_waits > div.td > div')[index + 1].text)

  def crossings(self):
    rows = self.__time_block.find_all('tr')
    return {x.find('td').text:BCFerriesCrossing(self.name, x, self.__api) for x in rows}


