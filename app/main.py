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
    print 'START'
    data = bottle.request.json

    myID = data['you']['id']
    gameID = data['game']['id']
    height = data['board']['height']
    width = data['board']['width'] 

    print '-----------------'
    print 'gameID: ', gameID
    print 'myID: ', myID
    print 'height: ', height
    print 'width: ', width
    print '-----------------'

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
    print "HEAD COORDS: ", headCoords
    x = headCoords['x']
    y = headCoords['y']
    if x == 0:
        validDirections.remove('left')
        print 'cant go left'

    if x == width-1 :
        validDirections.remove('right')
        print 'cant go right'

    if y == 0:
        validDirections.remove('up')
        print 'cant go up'

    if y == height-1:
        validDirections.remove('down')
        print 'cant go down'

'''
TODO
Eliminates return values that would run us into our own body
or that of another snake

def elimBodyCollide(headCoords):
    x = headCoords['x']
    y = headCoords['y']
    
    niceTypes = ['food', 'empty']

    if x < width-1:
        type = boardMap[x+1][y]['type']
        if type not in niceTypes:
            validDirections.remove('right')

    if y < height-1:
        type = boardMap[x][y+1]['type']
        if type not in niceTypes:
            validDirections.remove('down')

    if x > 0:
        type = boardMap[x-1][y]['type']
        if type not in niceTypes:
            validDirections.remove('left')
    
    if y > 0:
        type = boardMap[x][y-1]['type']
        if type not in niceTypes:
            validDirections.remove('up')
'''

def elimBodyCollide(headCoord, data):

    x = headCoord['x']
    y = headCoord['y']
    toCheck = [{'x' : x-1, 'y':y}, {'x' : x+1, 'y':y}, {'x' : x, 'y':y-1}, {'x' : x, 'y':y+1}]

    bodies = data['you']['body']
    for snake in data['board']['snakes']:
        bodies.extend(snake['body'])
    
    for coord in toCheck:
        if coord in bodies:
            toCheck.remove(coord)

    if {'x' : x-1, 'y':y} not in toCheck:
        if 'left' in validDirections:
            validDirections.remove('left')
            print 'cant go left'

    if {'x' : x+1, 'y':y} not in toCheck:
        if 'right' in validDirections:
            validDirections.remove('right')
            print 'cant go right'

    if {'x' : x, 'y':y-1} not in toCheck:
        if 'up' in validDirections:
            validDirections.remove('up')
            print 'cant go up'

    if {'x' : x, 'y':y+1} not in toCheck:
        if 'down' in validDirections:
            validDirections.remove('down')
            print 'cant go down'

    # want a list of our body items and others all together


# ====================== GLOBALS ==========================

gameID = ''
myID = ''

height = 0 
width = 0

directions = ['up', 'left', 'down', 'right']
validDirections = []

'''
type can be body, head, food, or empty
if type is body or head, dict will also have an id field

ex - boardMao[0][0] = {'type' : head, id : '12412412310'}

'''
# boardMap = [[{'type': '', 'id' : ''} for x in range(width)] for y in range(height)] 


# ======================= Build Table ============================
'''
def makeBoardMap(data):
    
    # empties
    for x in range(width):
        for y in range(height):
            boardMap[x][y]['type'] = 'empty'

    # food
    for coord in data['board']['food']:
        boardMap[coord['x']][coord['y']]['type'] = 'food'

    # other snakes
    for snake in data['board']['snakes']:
        id = snake['id']
        flag = True
        for coord in snake[body]:
            if(flag):
                falg = False
                boardMap[coord['x']][coord['y']]['type'] = 'head'
            else:                            
                boardMap[coord['x']][coord['y']]['type'] = 'body'            
            boardMap[coord['x']][coord['y']]['id'] = id            

    # my snake 
    for coord in data['you'][body]:
        boardMap[coord['x']][coord['y']]['type'] = 'you'
'''

# ======================= MOVE ============================

@bottle.post('/move')
def move():
    print 'move received'
    data = bottle.request.json 
    you = data['you']

    print 'turn {}'.format(data['turn']) 
    validDirections = directions[:] # reset on each turn
    # boardMap = [[0 for x in range(width)] for y in range(height)]

    # makeBoardMap(data)

    # elimRunoff(you['body'][0])
    # elimBodyCollide(you['body'][0])
    # elimBodyCollide(you['body'][0], data)





    response = directions[(data['turn']/2) % 4]

    # if len(validDirections) > 0:
    #     response = random.choice(validDirections)
    # else: 
    #     response = 'down' #gg

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
