import collections, functools32
from Levenshtein import ratio

class FuzzyDict(collections.MutableMapping):
  def __init__(self, *args, **kwargs):
    self.d = dict()
    self.update(dict(*args, **kwargs))

  @functools32.lru_cache(128)
  def __get_best_match(self, key):
    key = unicode(key)
    return max(map(lambda x: (x, ratio(x, key)), self.d.keys()), key=lambda x: x[1])

  def __getitem__(self, key):
    if key in self.d:
      return self.d[key]
    result = self.__get_best_match(key)
    if result and result[1] > 0.5:
      return self.d[result[0]]
    else:
      raise KeyError(key)

  def __setitem__(self, key, value):
    self.d[key] = value

  def __delitem__(self, key):
    del self.d[key]

  def __iter__(self):
    return iter(self.d)

  def __len__(self):
    return len(self.d)

  def __hash__(self):
    return hash(frozenset(self.d.items()))

  def __str__(self):
    return str(self.d)

  def __repr__(self):
    return repr(self.d)
