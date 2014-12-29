def to_int(s):
  try:
    return max(int(s), 0)
  except:
    return 0
