import random, pygame, sys, copy
from pygame.locals import *

from Mech_Functions4 import *
from Mech_Classes_4 import *


FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 860 # size of window's width in pixels
WINDOWHEIGHT = 700 # size of windows' height in pixels

TILESIZE = 40 # size of box height & width in pixels
GAPSIZE = 5 # size of gap between tiles in pixels
BOARDWIDTH = 10 # number of columns of spaces
BOARDHEIGHT = 10 # number of rows of space

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (TILESIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (TILESIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)

GRASS =    (  0, 200,   0)

BGCOLOR = WHITE
GRIDCOLOR = BLACK



##### Unit Symbols

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

Symbols = {  DONUT    : 'donut',
             SQUARE   : 'square',
             DIAMOND  : 'diamond',
             LINES    : 'lines',
             OVAL     : 'oval'     }


############ Create Combatants
Alpha = Mech(name = 'User', health = 8, speed = 3,location = (int(BOARDWIDTH/2), BOARDHEIGHT -1), symbol = DONUT, weapons = [Laser()])
Beta = Mech(name = 'Beta', health = 8, speed = 3,location = (int(BOARDWIDTH/2),  0), symbol = SQUARE, weapons = [Laser()])
#Beta = Mech(name = 'Beta', health = 4, speed = 3,location = (int(BOARDWIDTH/2), 0), symbol = SQUARE, weapons = [Laser()])

#Alpha = Mech(name = 'User', health = 20, speed = 3,location = (gridsize[0]-3,int(gridsize[1]/2)), symbol = 'U', weapons = [Laser()])
Charlie = Mech(name = 'Charlie', health = 8, speed = 3,location = (BOARDWIDTH-1,int(BOARDWIDTH/2)), symbol = DIAMOND, weapons = [Laser()])

combatants = [Alpha, Beta, Charlie]


numInitialCombatants = len(combatants)
TOPMARGIN = (10 +TILESIZE) * numInitialCombatants + 10


def main(combatants):
    global FPSCLOCK, DISPLAYSURF, STATUSFONT, NEW_SURF, NEW_RECT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    STATUSFONT = pygame.font.Font('freesansbold.ttf', 30)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Mech Game')

    NEW_SURF, NEW_RECT = makeText('New Game', BLACK, BLUE, 20, WINDOWHEIGHT - 90)

    mainBoard = createTileMap()

    gameActive = True
    firstSelection = None # stores the (x, y) of the first box clicked.
    status = ''
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    combatantTurn = 0 # Starts with first combatant and increases when he runs out of turns
    turn = 0  #Start out at turn 0 but tells people one bc index at 0
    aliveCombatants = copy.deepcopy(combatants) ####Creates a copy of the list of combatants.  Helps on reset and can modify the lists

    while gameActive: # game is being played
        mouseClicked = False

        ### Determine who's turn it is ####
        unit = aliveCombatants[combatantTurn]
        userTurn = (unit.name == 'User')

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, unit, turn, status, aliveCombatants)

        ############ event handling loop ##################
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                if NEW_RECT.collidepoint(event.pos): #Restarts the game with original combatants and creates a new tilemap
                    aliveCombatants = copy.deepcopy(combatants)
                    mainBoard = createTileMap()
                    combatantTurn = 0
                    turn = 0

                mousex, mousey = event.pos
                mouseClicked = True


        tilex, tiley = getTileAtPixel(mousex, mousey)
        combatantLocations = getCombatantLocations(aliveCombatants)

        #### Computer's Turn ####
        if not userTurn:
            status = computerTurn(unit, aliveCombatants, (BOARDWIDTH, BOARDHEIGHT))
            turn += 1
            if turn >= unit.speed: #Unit used up all of his turns
                combatantTurn += 1
                turn = 0

        ##User's Turn ###
        elif tilex != None and tiley != None:  #Mouse is over a tile
            if (tilex, tiley) in combatantLocations: #If there is a combatant here
                drawHighlightTile(tilex, tiley, RED)
                enemy = identifyCombatant(tilex, tiley, aliveCombatants)
                drawIntel(tilex, tiley, unit, enemy)
                if userTurn and mouseClicked: #Don't need userTurn bc we are in the elif, but good double check  #We Fired
                    status = unit.Attack(enemy, 0) #Hard coded right now that you can only use weapon 1
                    turn += 1


            else:
                drawHighlightTile(tilex, tiley, YELLOW)
                if userTurn and mouseClicked:     #Movement
                    distance = abs(unit.location[0] - tilex) + abs(unit.location[1]-tiley)
                    if distance <= unit.speed - turn:
                        turn += distance
                        status = (str(unit.name) + ' moved ' + str(distance))
                        unit.location = (tilex,tiley)
                    else:
                        status = ('Invalid Move: Cannot move that far')
        if turn >= unit.speed: #Unit used up all of his turns
            combatantTurn += 1
            turn = 0

        aliveCombatants, combatantTurn = updateCombatants(aliveCombatants, combatantTurn)

        pygame.display.update() #Needs to update display after the user's turn so the highlighted boxes are shown

        if victoryCondition(aliveCombatants): #Can we have a status display showing who won?
            DISPLAYSURF.fill(BGCOLOR) #Redraws everything so we have the most recent status of who destroyed who
            drawBoard(mainBoard, unit, turn, status, aliveCombatants)
            pygame.display.update()
            pygame.time.wait(1000) #pause to see last status update
            status = (aliveCombatants[combatantTurn].name + ' WON!!!!!')
            gameActive = False

        if not userTurn: #### Pauses after the computer move to see what happened
            pygame.time.wait(2000)

        FPSCLOCK.tick(FPS)

    while True: # Someone Won so waiting for the player to start a new game or exit
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, unit, turn, status, aliveCombatants)

        ############ event handling loop ##################
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                if NEW_RECT.collidepoint(event.pos): #Restarts the game with original combatants and creates a new tilemap
                    main(combatants)
                mousex, mousey = event.pos
                mouseClicked = True
        pygame.display.update()
########################################

def drawStatus(status):
    textObj = STATUSFONT.render(status,  True, BLACK, BGCOLOR)
    DISPLAYSURF.blit(textObj, (XMARGIN,(TOPMARGIN + ((TILESIZE + GAPSIZE) *BOARDHEIGHT + GAPSIZE) +10)+ TILESIZE))

def drawBoard(tilemap, currentMech, turn, status, aliveCombatants):
    # Draws background grid and then puts pieces on top
    pygame.draw.rect(DISPLAYSURF, GRIDCOLOR, (XMARGIN, TOPMARGIN, (TILESIZE+GAPSIZE) * BOARDWIDTH + GAPSIZE, (TILESIZE+GAPSIZE) * BOARDHEIGHT + GAPSIZE))
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left , top = leftTopCoordsOfTile(tilex, tiley)
            color, elevation = getColorAndElevation(tilemap, tilex, tiley)
            pygame.draw.rect(DISPLAYSURF, color, (left, top, TILESIZE, TILESIZE))

    for i in range(len(aliveCombatants)):
        placePositionX = 10 + XMARGIN
        placePositionY = (10 +TILESIZE) * i + 10
        mech = aliveCombatants[i]
        team = mech.team
        if team == None:   ###### NEED TO ADD TEAM COLOR
            color = GRAY
        shape = mech.symbol

        drawSymbolPixel(shape, color, placePositionX, placePositionY)#BOARDHEIGHT *TILESIZE -20) ### Draw Symbol works off Tiles not pixels


        #DISPLAYSURF.blit(texture,(placePosition, BOARDHEIGHT *TILESIZE +20))
        placePositionX += (TILESIZE + 10)
        textObj = STATUSFONT.render(str(mech.name) + '     /    HEALTH   ' + \
                                    str(mech.health) , True, BLACK, BGCOLOR)
        #DISPLAYSURF.blit(textObj, (placePositionX, YMARGIN / 2))
        DISPLAYSURF.blit(textObj, (placePositionX, placePositionY + TILESIZE/5))

    textObj = STATUSFONT.render('Turn ' +str(turn +1)+ ' of ' + str(currentMech.speed) + \
                                ' for ' +str(currentMech.name) , True, BLACK, BGCOLOR)# + ' of ' + str(currentMech.speed))
    DISPLAYSURF.blit(textObj, (XMARGIN,TOPMARGIN + ((TILESIZE + GAPSIZE) *BOARDHEIGHT + GAPSIZE) +10))

    textObj = STATUSFONT.render(status,  True, BLACK, BGCOLOR)
    DISPLAYSURF.blit(textObj, (XMARGIN,(TOPMARGIN + ((TILESIZE + GAPSIZE) *BOARDHEIGHT + GAPSIZE) +10)+ TILESIZE))
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)

    for mech in aliveCombatants:
        tilex, tiley = mech.location[0], mech.location[1]
        team = mech.team
        if team == None:   ###### NEED TO ADD TEAM COLOR
            color = GRAY
        shape = mech.symbol
        drawSymbol(shape, color, tilex, tiley)


def createTileMap():
    # Create the board data structure, Currently only Grass and Elevation of 1
    # Potential make the terrain type a class with grass and instance which can have unique properties
    tilemap = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append((GRASS, 1)) #### Default adding GRASSCOLOR AND ELEVATION 1
        tilemap.append(column)
    return tilemap


def getTileAtPixel(x, y):
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfTile(tilex, tiley)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tilex, tiley)
    return (None, None)

def drawHighlightTile(tilex, tiley, color):
    left, top = leftTopCoordsOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, color, (left - GAPSIZE, top - GAPSIZE, TILESIZE + 2 * GAPSIZE, TILESIZE + 2 * GAPSIZE), 4)

def getColorAndElevation(tilemap, tilex, tiley):
    # color value for x, y spot is stored in board[x][y][0]
    # elevation value for x, y spot is stored in board[x][y][1]
    return tilemap[tilex][tiley][0], tilemap[tilex][tiley][1]

def leftTopCoordsOfTile(tilex, tiley):
    # Convert board coordinates to pixel coordinates
    left = tilex * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE #Add gapsize at end bc want tile in middle of grid
    top = tiley * (TILESIZE + GAPSIZE) + TOPMARGIN + GAPSIZE
    return (left, top)

def identifyCombatant(tilex, tiley, combatants):
    for mech in combatants:
        if (tilex, tiley) == mech.location:
            enemyMech = mech
    return enemyMech

def drawIntel(tilex, tiley, unit, mechIntel):
    #mechIntel = combatants[0]
    team = mechIntel.team
    if team == None:   ###### NEED TO ADD TEAM COLOR
        color = GRAY

    intelPositionX = WINDOWWIDTH - XMARGIN + 10# Starts 10 pixels from end of board
    intelPositionY = TOPMARGIN + GAPSIZE

    shape = mechIntel.symbol
    drawSymbolPixel(shape, color, intelPositionX, intelPositionY)#BOARDHEIGHT *TILESIZE -20) ### Draw Symbol works off Tiles not pixels

    textObj = STATUSFONT.render(str(mechIntel.name), True, BLACK, BGCOLOR)
    DISPLAYSURF.blit(textObj, (intelPositionX + (TILESIZE + 10), intelPositionY + TILESIZE/5))

    intelPositionY += (TILESIZE + GAPSIZE)
    textObj = STATUSFONT.render('Health      ' + str(mechIntel.health), True, BLACK, BGCOLOR)
    DISPLAYSURF.blit(textObj, (intelPositionX, intelPositionY + TILESIZE/5))

    intelPositionY += (TILESIZE + GAPSIZE)
    textObj = STATUSFONT.render('Speed       ' + str(mechIntel.speed), True, BLACK, BGCOLOR)
    DISPLAYSURF.blit(textObj, (intelPositionX, intelPositionY + TILESIZE/5))

    intelPositionY += (TILESIZE + GAPSIZE)
    textObj = STATUSFONT.render('Distance  ' + str(unit.weaponDistance(mechIntel)), True, BLACK, BGCOLOR)
    DISPLAYSURF.blit(textObj, (intelPositionX, intelPositionY + TILESIZE/5))



def drawSymbolPixel(shape, color, left, top):
    quarter = int(TILESIZE * 0.25)
    half =    int(TILESIZE * 0.5)
    ### Draw the symbols
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, TILESIZE - half, TILESIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + TILESIZE - 1, top + half), (left + half, top + TILESIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, TILESIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + TILESIZE - 1), (left + TILESIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, TILESIZE, half))


def drawSymbol(shape, color, tilex, tiley):
    quarter = int(TILESIZE * 0.25)
    half =    int(TILESIZE * 0.5)
    left, top = leftTopCoordsOfTile(tilex, tiley)
    ### Draw the symbols
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, TILESIZE - half, TILESIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + TILESIZE - 1, top + half), (left + half, top + TILESIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, TILESIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + TILESIZE - 1), (left + TILESIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, TILESIZE, half))

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = STATUSFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

if __name__ == '__main__':
    main(combatants)
