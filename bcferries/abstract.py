import json
from fuzzydict import FuzzyDict

class BCFerriesAbstractObject(object):
  def __init__(self, *args, **kwargs):
    self.__props = {'name'}

  def __str__(self):
    return "{}({})".format(self.__class__.__name__, self.name)

  def __repr__(self):
    return self.__str__()

  def _register_properties(self, props):
    self.__props.update(props)

  def to_dict(self, fuzzy=False):
    d = {}
    dict_f = FuzzyDict if fuzzy else dict
    operations = [
      lambda x: x(),
      lambda x: dict_f({k:v.to_dict() for k,v in x.items()}),
      lambda x: [v.to_dict() for v in x],
      lambda x: x.to_dict(),
      lambda x: x.isoformat()
    ]
    for prop in self.__props:
      val = getattr(self, prop)
      for operation in operations:
        try:
          val = operation(val)
        except:
          pass
      d[prop] = val
    return d

  def to_fuzzy_dict(self):
    return FuzzyDict(self.to_dict(fuzzy=True))

  def to_json(self):
    return json.dumps(self.to_dict())
