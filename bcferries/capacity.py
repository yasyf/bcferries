from abstract import BCFerriesAbstractObject
from urlparse import urlparse, parse_qs

class BCFerriesCapacity(BCFerriesAbstractObject):
  def __init__(self, a):
    super(BCFerriesCapacity, self).__init__(self)

    percents = parse_qs(urlparse(a.get('href')).query)['est'][0].split(',')
    self.filled = int(percents[0])
    self.mixed_filled = int(percents[1])
    self.passenger_filled = int(percents[2])
    self.name = "{}% Full".format(percents[0])

    self._register_properties(['filled', 'mixed_filled', 'passenger_filled'])
