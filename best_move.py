from utils import assign, getBodies, getHeads, getPossibleMoves, safe, onlyOneWayToGo, indvBodies, areas_near_heads, smaller_snakes_get_heads, get_dangerous_heads, i_am_closest
from get_closest import closest
from corner_snake import tryCorner, can_trap
from maths import distance_between
from try_other_snakes import others_can_corner_me, other_can_trap
def best_move(data, scores):
  moves = ['up', 'down', 'left', 'right']
  dict_moves = assign(data['you']['head'])
  points_moves = [150, 150, 150, 150]
  #print('DICT MOVES:', dict_moves)
  bodies = getBodies(data)
  heads = getHeads(data)
  myhead = data['you']['head']
  mybody = data['you']['body']
  #mytail = data['you']['body'][len(data['you']['body']) - 1]
  food = data['board']['food']
  health = data['you']['health']
  height = data['board']['height']
  width = data['board']['width']
  snakes = data['board']['snakes']
  center = {
    'x':round(width/2),
    'y':round(height/2)
  }
  small_heads = smaller_snakes_get_heads(data)
  indv_bodies = indvBodies(data)
  head_areas = areas_near_heads(small_heads, indv_bodies, mybody, myhead)
  danger_heads = get_dangerous_heads(data)
  me_smallest = 0
  for snake in snakes:
    if len(snake['body']) >= len(mybody):
      me_smallest +=1
  if me_smallest == len(snakes):
    me_smallest = 2
  else:
    me_smallest = 1/3
  #print('AM I THE SMALLEST?', me_smallest)
  best_move_for_space = None
  num_best_move_space = 0
  for trymoves in dict_moves:
    thismoves = getPossibleMoves(bodies, trymoves, data, mybody)
    if thismoves > num_best_move_space:
      num_best_move_space = thismoves
      best_move_for_space = trymoves
  #print(num_best_move_space)
  for a in range(4):
    if dict_moves[a] in bodies or not -1<dict_moves[a]['x']<width or not -1<dict_moves[a]['y']<height:
      points_moves[a] -= scores[0] #350
    print('MOVESCORE FOR '+ moves[a]+ ' SO FAR: '+ str(points_moves[a]))
    if safe(dict_moves[a], heads, indv_bodies, myhead, mybody) == []:
      
      first_time = getPossibleMoves(bodies, dict_moves[a], data, mybody, num_best_move_space <= len(mybody))

      popthese = []
      body_copy = []
      bodies_copy = []
      for minibody in mybody:
        body_copy.append(minibody)
      for hh in bodies:
        bodies_copy.append(hh)
      for h in range(first_time):
        try:
          popthese.append(body_copy[len(body_copy) - 1])
          body_copy.pop(len(body_copy) - 1)
        except:
          pass
      for elem in popthese:
        if elem in bodies_copy:
          bodies_copy.pop(bodies_copy.index(elem))
      #move_count = getPossibleMoves(bodies_copy, dict_moves[a], data, body_copy, num_best_move_space <= len(mybody), True)
      points_moves[a] += (first_time - len(mybody)*scores[1]) #1.5
      print("MOVES AVAILABLE FOR MOVE", moves[a], ': ' + str(first_time))
      #print('MOVES INTERPRETTED AS:', (move_count - len(mybody)*scores[1]))
      
      points_moves[a] -= scores[2]
    else:
      points_moves[a] -= 200 #70
      #print(moves[a], "IS NOT SAFE!!!!!")
    print('MOVESCORE FOR', moves[a], 'SO FAR:', points_moves[a])
    food_runtime = 0
    if me_smallest == 2 or health < 46:
      for foodcoord in food:
        if i_am_closest(heads, dict_moves[a], foodcoord):

          if foodcoord == dict_moves[a]:
            print('  RIGHT ON TOP OF FOOD!')
            points_moves[a] +=50
          elif distance_between(foodcoord, dict_moves[a]) == 1:
            points_moves[a] +=40
          else:
            points_moves[a] += 5
          food_runtime +=1
      if food_runtime == 0:
        points_moves[a] -= len(food) * 3
      print('FOODSCORE!!! FOR', moves[a], 'SO FAR:', points_moves[a])
    #print('TRYING TO CLONK A HEAD...')
      #points_moves[a] += scores[4] + 30 #60
    #print("SMALL HEADS LENGTH:", len(head_areas))
    if me_smallest !=2:
      for smallhead in heads:
        avg = (width + height) / 2
        points_moves[a] += ((2 * avg) - (distance_between(dict_moves[a], smallhead))) * 2.5
        #print('FOR MOVE:', moves[a] + ", THE DISTANCE TO THIS HEAD IS", distance_between(dict_moves[a], myhead))
    else:
      for smallhead in small_heads:
        avg = (width + height) / 2
        points_moves[a] += (2 * avg) - (distance_between(dict_moves[a], smallhead)) * 2.5
        #print('FOR MOVE:', moves[a] + ", THE DISTANCE TO THIS HEAD IS", distance_between(dict_moves[a], myhead))
    i_can_corner = False
    if tryCorner(heads, myhead, dict_moves[a], data):
      points_moves[a] +=scores[5] + 25 #60
      print('MOVE:', moves[a], '........GET CORNERED HA YOU THOUGHT')
      i_can_corner = True
    if dict_moves[a] in head_areas:
      print('ON MOVE', moves[a], "I CAN (probably) HIT A HEAD!")
      #60
      points_moves[a] +=scores[6] + (10 - distance_between(myhead, center)) * 1.2
    for snakehead in snakes:
      if not i_can_corner:
        if others_can_corner_me(data, dict_moves[a], snakehead['head']) and not snakehead['head'] == myhead:
          print('ON MOVE', moves[a], 'I MIGHT GET CORNERED')
          points_moves[a] -=scores[7] #70
      if can_trap(data, heads, dict_moves[a]):
        points_moves[a] +=scores[8] #55
      if other_can_trap(data, dict_moves[a], snakehead['head']) <= len(mybody):
        points_moves[a] -=70
    
    for danger in danger_heads:
      if distance_between(danger, myhead) * 2 <=4.5:
      #swcores[9] = 2.5
        points_moves[a] +=distance_between(danger, myhead) * scores[9]
      else:
        points_moves[a] +=scores[9] + 3
    
    if num_best_move_space <= len(mybody)/2:
      print('STATUS: TRAPPED\nTRYING TO CONSERVE SPACE...')
      if dict_moves[a] == best_move_for_space:
        points_moves[a] +=scores[10] #60
      

  print('MOVESCORES:', points_moves)
  print('MOVES:', moves)
  print(f"Best move is {moves[points_moves.index(max(points_moves))]} with a score of {max(points_moves)}")
  return moves[points_moves.index(max(points_moves))]
  
  
