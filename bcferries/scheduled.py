from abstract import BCFerriesAbstractObject
from helpers import to_int
import dateutil.parser, datetime, re

time_regex = re.compile(r'(\d) HOURS?(?: (\d{1,2}) MINUTES?)?')

class BCFerriesScheduledCrossing(BCFerriesAbstractObject):
  def __init__(self, name, sailing_time, time_row):
    super(BCFerriesScheduledCrossing, self).__init__(self)

    scheduled_dep, actual_dep, arrival, status, _ = time_row
    self.boat_name = name
    self.name = '{} at {}'.format(name, scheduled_dep)
    self.status = status.strip()

    self.sailing_time = 0
    match = time_regex.match(sailing_time)
    if match:
      hours, minutes = match.group(1, 2)
      self.sailing_time = datetime.timedelta(minutes=to_int(minutes), hours=to_int(hours))

    self.scheduled_departure = dateutil.parser.parse(scheduled_dep, fuzzy=True) if scheduled_dep else None
    self.actual_departure = dateutil.parser.parse(actual_dep, fuzzy=True) if actual_dep else None
    self.arrival = dateutil.parser.parse(arrival, fuzzy=True) if arrival else None

    self.__fake_actual_departure = self.actual_departure or self.scheduled_departure

    self._register_properties(['boat_name', 'sailing_time', 'scheduled_departure', 'actual_departure', 'arrival'])

  def is_early(self):
    return self.__fake_actual_departure < self.scheduled_departure

  def is_late(self):
    return self.__fake_actual_departure > self.scheduled_departure

  def is_departed(self):
    return self.__fake_actual_departure <= datetime.datetime.now()

  def delta_from_schedule(self):
    if self.is_early():
      return self.scheduled_departure - self.__fake_actual_departure
    else:
      return self.__fake_actual_departure - self.scheduled_departure
