import bottle
import os
from datetime import datetime
from best_move import best_move
from colored import fore, back, style
def getretDate():
  this = datetime.now()
  this = str(this)
  this = this.split(" ")
  this = this[1].split(":")
  for i in range(len(this)):
    this[i] = float(this[i])
  return this
def comparedate(one, two):
  diff =  [
    two[2] - one[2],
    two[1] - one[1],
    two[0] - one[0]
  ]
  diff.reverse()
  return diff


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    #placeholder = open(data['game']['id'] + '.txt', 'w')
    return "/start"

    # TODO: Do things with data

@bottle.get('/')
def metadata():
    return {
        'color': '#FDAC53',
        'author': 'DAChenScratch',
        'apiversion':"1",
        'version':'1.14 Alpha',
        "head":"smile",
        "tail":"round-bum",
    }

@bottle.post('/move')
def move():
    data = bottle.request.json
    scores = [
      350, 1.5, 70, 1.3, 60, 60, 60, 70, 55, 2.5, 60
    ]
    print(f"TURN NUMBER: {data['turn']}")
    first = getretDate()
    move = best_move(data, scores)
    second = getretDate()
    time_spent = comparedate(first, second)
    print(f"MOVE: {move}")
    print(f"MOVE {data['turn']} TOOK {time_spent[2] * 1000} milliseconds.")
    print(fore.LIGHT_BLUE + back.RED + style.BOLD + f"MOVE {data['turn']} TOOK {time_spent[2] * 1000} milliseconds." + style.RESET)
    return {"move": move}

@bottle.post('/end')
def end():
  data = bottle.request.json
  names = 'Snake names are: '
  for snake in data['board']['snakes']:
    if data['board']['snakes'].index(snake) != len(data['board']['snakes']) - 1:
      names =  names + snake['name'] + ', '
    else:
      if not len(data['board']['snakes']) == 1:
        names = names + 'and ' + snake['name'] + '.'
      else:
        names = names  + snake['name'] + '.'
  #os.system('clear')
  print('SNAKES REMAINING:', len(data['board']['snakes']))
  print(names)
  if len(data['board']['snakes']) == 1 and names == 'Snake names are: Marigold.':
    print('YEAH!!! VICTORY!!!')
  else:
    print('\n\n\n\nF in the terminal I lost.')
  return "hi"
# Expose WSGI app (so gunicorn can find it)



application = bottle.default_app()
bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))

