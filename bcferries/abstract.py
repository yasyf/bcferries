import json
from functools import wraps
from api import BCFerriesAPI
from fuzzydict import FuzzyDict

class BCFerriesAbstractObject(object):
  def __init__(self, *args, **kwargs):
    self.__props = {'name'}

  def __str__(self):
    return "{} ({})".format(self.__class__.__name__, self.name)

  def __repr__(self):
    return self.__str__()

  def _register_properties(self, props):
    self.__props.update(props)

  def to_dict(self):
    d = {}
    for prop in self.__props:
      val = getattr(self, prop)
      operations = [
        lambda x: x(),
        lambda x: FuzzyDict({k:v.to_dict() for k,v in x.items()}),
        lambda x: [v.to_dict() for v in x],
        lambda x: x.to_dict(),
        lambda x: x.isoformat()
      ]
      for operation in operations:
        try:
          val = operation(val)
        except:
          pass
      d[prop] = val
    return d

  def to_fuzzy_dict(self):
    return FuzzyDict(self.to_dict())

  def to_json(self):
    return json.dumps(self.to_dict())

def cacheable(f):
  @wraps(f)
  def wrapper(self, *args, **kwargs):
    ignore_cache = kwargs.pop('ignore_cache', False)
    if ignore_cache is True:
      BCFerriesAPI.ignore_cache = True
      result = f(self, *args, **kwargs)
      BCFerriesAPI.ignore_cache = False
      return result
    else:
      return f(self, *args, **kwargs)
  return wrapper

def fuzzy(f):
  @wraps(f)
  def wrapper(self, *args, **kwargs):
    result = f(self, *args, **kwargs)
    return FuzzyDict(result)
  return wrapper
