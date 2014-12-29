from abstract import BCFerriesAbstractObject
import dateutil.parser, datetime

class BCFerriesScheduledCrossing(BCFerriesAbstractObject):
  def __init__(self, name, sailing_time, time_row):
    super(BCFerriesScheduledCrossing, self).__init__(self)

    scheduled_dep, actual_dep, arrival, status, _ = time_row
    self.name = '{} at {}'.format(name, scheduled_dep)
    self.status = status.strip()
    self.sailing_time = sailing_time
    self.scheduled_departure = dateutil.parser.parse(scheduled_dep, fuzzy=True) if scheduled_dep else None
    self.actual_departure = dateutil.parser.parse(actual_dep, fuzzy=True) if actual_dep else None
    self.arrival = dateutil.parser.parse(arrival, fuzzy=True) if arrival else None

    self._register_properties(['sailing_time', 'scheduled_departure', 'actual_departure', 'arrival'])

  def is_early(self):
    return (self.actual_departure or self.scheduled_departure) < self.scheduled_departure

  def is_late(self):
    return (self.actual_departure or self.scheduled_departure) > self.scheduled_departure

  def is_departed(self):
    return (self.actual_departure or self.scheduled_departure) <= datetime.datetime.now()
