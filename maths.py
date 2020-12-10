import math
def sqr(x):
  return x * x
def distance_between(one, two):
  return math.sqrt(sqr(two["x"] - one["x"]) + sqr(two['y'] - one['y']))

def manhattan(one, two):
  return abs(two["x"] - one["x"]) + abs(two['y'] - one['y'])
