from utils import assign, getBodies, getPossibleMoves
from corner_snake import tryCorner
def others_can_corner_me(data, myhead, thishead):
  #moves[a]
  if thishead != myhead:
    moves = assign(thishead)
    for a in range(4):
      if tryCorner([myhead], thishead, moves[a], data):
        #print(f"THISHEAD {thishead}\nMYHEAD {myhead}")
        #if onlyOneWayToGo(data, myhead, False):
        return True
  return False

      



def other_can_trap(data, myhead, thisHead):
  moves = assign(thisHead)
  worst_scenario = 999999999
  for a in range(4):
    bodies = getBodies(data)
    bodies.append(moves[a])
    #first_time = getPossibleMoves(bodies, dict_moves[a], data, mybody)
    thismove = getPossibleMoves(bodies, myhead, data, data['you']['body'])
    if thismove < worst_scenario and thismove >0:
      #print('THIS MOVE', thismove)
      worst_scenario = thismove
  if worst_scenario <len(data['you']['body'])/2:
    return -40
  else:
    return 10
