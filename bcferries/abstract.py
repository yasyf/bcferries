import json, datetime
from fuzzydict import FuzzyDict
from geopy.location import Location
from geopy.distance import Distance

def try_with_kwargs(f, **kwargs):
  try:
    return f(**kwargs)
  except TypeError:
    return f()

def clean_special_types(x):
  if isinstance(x, Location):
    return list(x)
  if isinstance(x, Distance):
    return x.km
  if isinstance(x, datetime.timedelta):
    return x.seconds
  if hasattr(x, 'isoformat'):
    return x.isoformat()
  return x

class BCFerriesAbstractObject(object):
  def __init__(self, *args, **kwargs):
    self.__props = {'name'}

  def __str__(self):
    return "{}({})".format(self.__class__.__name__, self.name)

  def __repr__(self):
    return self.__str__()

  def _register_properties(self, props):
    self.__props.update(props)

  def to_dict(self, fuzzy=False, json=False, shallow=True):
    d = {}
    dict_f = FuzzyDict if fuzzy else dict
    operations = [
      lambda x: try_with_kwargs(x, keys_only=shallow),
      lambda x: dict_f({k:v.to_dict(fuzzy=fuzzy, json=json, shallow=shallow) for k,v in x.items()}),
      lambda x: [v.to_dict(fuzzy=fuzzy, json=json, shallow=shallow) for v in x],
      lambda x: x.to_dict(fuzzy=fuzzy, json=json, shallow=shallow),
      lambda x: clean_special_types(x) if json else x
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

  def to_fuzzy_dict(self, shallow=True):
    return FuzzyDict(self.to_dict(fuzzy=True, shallow=shallow))

  def to_json(self, shallow=True):
    return json.dumps(self.to_dict(json=True, shallow=shallow))
