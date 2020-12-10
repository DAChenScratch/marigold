from utils import onlyOneWayToGo, getBodies, trapped
def tryCorner(heads, myhead, target, data):
  width = data['board']['width']
  height = data['board']['height']
  bodies = getBodies(data)
  if target['x'] == myhead['x']:
    for b in range(myhead['x'], width):
      if {'x':b, 'y':target['y']} in heads and onlyOneWayToGo(data, {'x':b, 'y':target['y']}, False):
        return True
      elif {'x':b, 'y':target['y']} in bodies:
        return False
    for c in range(myhead['x'], -1, -1):
      if {'x':c, 'y':target['y']} in heads and onlyOneWayToGo(data, {'x':c, 'y':target['y']}, False):
        return True
      elif {'x':c, 'y':target['y']} in bodies:
        return False
    return False
      
  elif target['y'] == myhead['y']:
    for a in range(myhead['y'], height):
      if {'x':target['x'], 'y':a} in heads and onlyOneWayToGo(data, {'x':target['x'], 'y':a}, False):
        return True
      elif {'x':target['x'], 'y':a} in bodies:
        return False
    for d in range(myhead['y'], -1, -1):
      if {'x':target['x'], 'y':d} in heads and onlyOneWayToGo(data, {'x':target['x'], 'y':d}, False):
        return True
      elif {'x':target['x'], 'y':d} in bodies:
        return False
    return False
  else:
    return False
#trapped(bodies, target, width, height, shouldPrint

def can_trap(data, heads, target):
  #my target
  for head in heads:
    bodies = getBodies(data)
    bodies.append(target)
    if trapped(bodies, head, data, False):
      return True
    else:
      return False
