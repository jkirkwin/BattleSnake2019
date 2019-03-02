import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

# ======================= START ============================

@bottle.post('/start')
def start():
    print 'start received'
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    myID = data['you']['id']
    gameID = data['game']['id']
    height = data['board']['height']
    width = data['board']['width'] 

    print 'gameID: ', gameID
    print 'myID: ', myID

    color = "#FBE103"

    return start_response(color)

# =================== GET JSON RESPONSE ====================

def packageResponse(direction):
    json = '{ "move" : "%s"}'%direction
    print 'packaging {} as {}'.format(direction, json)
    return json

# ================== SIMPLE AVOID DEATH =====================

'''
Eliminates return values that would run us off the board
'''
def elimRunoff(headCoords):
    # headCoords = (x,y)
    print "HEAD COORDS: ", headCoords
    x = headCoords['x']
    y = headCoords['y']
    if x == 0:
        validDirections.remove('left')

    if x == width-1 :
        validDirections.remove('right')

    if y == 0:
        validDirections.remove('up')

    if y == height-1:
        validDirections.remove('down')

'''
TODO
Eliminates return values that would run us into our own body
or that of another snake
'''
def elimBodyCollide(snokes, yourBody, headCoords):
    x = headCoords['x']
    y = headCoords['y']

    # check own body first
    # for {bodyX, bodyY} in yourBody:

# ====================== GLOBALS ==========================

gameID = ''
myID = ''

height = 0 
width = 0

directions = ['up', 'down', 'left', 'right']
validDirections = []

'''
type can be body, head, food, or empty
if type is snake or head, dict will also have an id field

ex - boardMao[0][0] = {'type' : head, id : '12412412310'}

'''
boardMap = [[0 for x in range(width)] for y in range(height)] 



# ======================= MOVE ============================

@bottle.post('/move')
def move():
    print 'move received'
    data = bottle.request.json 
    you = data['you']

    validDirections = directions[:] # reset on each turn
    boardMap = [[0 for x in range(width)] for y in range(height)]

    elimRunoff(you['body'][0])


    response = random.choice(validDirections)

    # print data
    # print data['turn']

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    
    0,0 is top left
    """

    """
    Sanity TODO tasks
    
        Need a possible moves list that we can use before going on to anything more
        complicated

    1. Package the following functions into one that is called at start
       of move func to eliminate moves that would kill us.
       Can add to this if we have time to try to look ahead at some
       basic cases.
    - Stay on the board
    - Don't collide with your own body
    - Don't collide with other snakes' bodies

    2. Make sure you're getting food

    3. Handle case of possible head-on collisions -> check if a given cell
       is adjacent to another snake's head. Go there if all adjacent snake 
       heads belong to smaller snakes, otherwise eliminate this as a possibility

    """

    return packageResponse(response)


@bottle.post('/end')
def end():
    print 'end received'
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    # print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
