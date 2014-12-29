import datetime
from functools import wraps
from fuzzydict import FuzzyDict

def cacheable(f):
  @wraps(f)
  def wrapper(self, *args, **kwargs):
    ignore_cache = kwargs.pop('ignore_cache', False)
    if ignore_cache is True:
      self._api.ignore_cache = True
      result = f(self, *args, **kwargs)
      self._api.ignore_cache = False
      return result
    else:
      if (datetime.datetime.now() - self._api.last_cleared) > self._api.cache_for:
        self._api._flush_cache()
      return f(self, *args, **kwargs)
  return wrapper

def fuzzy(f):
  @wraps(f)
  def wrapper(self, *args, **kwargs):
    result = f(self, *args, **kwargs)
    return FuzzyDict(result)
  return wrapper

def lazy_cache(f):
  name = "__" + f.__name__
  def wrapper(self, *args, **kwargs):
    if not hasattr(self, name):
      setattr(self, name, f(self, *args, **kwargs))
    return getattr(self, name)
  return wrapper
