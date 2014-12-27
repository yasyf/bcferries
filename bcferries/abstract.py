class BCFerriesAbstractObject(object):
  def __str__(self):
    return "{} ({})".format(self.__class__.__name__, self.name)

  def __repr__(self):
    return self.__str__()
