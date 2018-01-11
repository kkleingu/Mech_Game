import random, os, math, time
from Mech_Functions2 import *
from Mech_Classes import *

########## Actual Game ############

game = True 
while(game):

###### Game Setup ######
    gridsize = (10,10)

    #Alpha = Mech(name = 'User', health = 20, speed = 1,location = (0,int(gridsize[1]/2)), symbol = 'U', weapons = [Laser()])
    #Beta = Mech(name = 'Beta', health = 4, speed = 3,location = (gridsize[0]-1,int(gridsize[1]/2)), symbol = 'X', weapons = [Laser()])
    #Alpha = Mech(name = 'User', health = 20, speed = 3,location = (gridsize[0]-3,int(gridsize[1]/2)), symbol = 'U', weapons = [Laser()])
    #Charlie = Mech(name = 'Charlie', health = 8, speed = 3,location = (gridsize[0]-1,2), symbol = 'O', weapons = [Laser()])

    Alpha = Gladiator(name = 'User', location = (0,int(gridsize[1]/2)), symbol = 'U')
    Beta = Cricket(name = 'Beta', location = (gridsize[0]-1,int(gridsize[1]/2)), symbol = 'X')
    #Alpha = Mech(name = 'User', health = 20, speed = 3,location = (gridsize[0]-3,int(gridsize[1]/2)), symbol = 'U', weapons = [Laser()])
    Charlie = Cricket(name = 'Charlie', location = (gridsize[0]-1,2), symbol = 'O')
    Delta = Cricket(name = 'Delta', location = (gridsize[0]-1,2), symbol = 'D')


    Red = Team('RED', [Beta, Charlie])
    Combatants = [Alpha, Beta, Charlie, Delta]

    movements = {'W':(-1,0), 'A': (0,-1), 'S' : (1,0), 'D' : (0,1), 'Q':(0,0)}

##### Game #####
    
    grid = [['.' for _ in range(gridsize[0])] for _ in range(gridsize[1])]
    placeUnits(grid, Combatants)          
    printMap(grid, Combatants)
    
    match = True
   
    while(match):
        tempCombatants = Combatants
        for unit in Combatants: 
            for turn in range(unit.speed):    ####### Every Turn per Combatant
                print('TURN \t%d of %d' % ((turn+1),unit.speed))
                if unit.name == 'User':
                    playerTurn(unit, movements, tempCombatants, grid)
                else:
                    print('% s IS MOVING' % unit.name)
                    computerTurn(unit, movements, tempCombatants, grid)
                tempCombatants = []
                for x in Combatants: #Check if dead
                    if x.health > 0:
                        tempCombatants.append(x)
                updateMap(grid, tempCombatants)
                if not victoryCondition(tempCombatants):
                    match = False
                    break
            if tempCombatants != Combatants:
                Combatants = list(tempCombatants)
                combatantnames = []
                for i in Combatants:
                    combatantnames.append(i.name)
                lastusernumber = combatantnames.index(unit.name)
                Combatants = Combatants[lastusernumber +1:len(Combatants)] + Combatants[0:lastusernumber+1] #Reorders to put the last user at the end of the list
                break
    choice = 'X' 
    while(choice.upper() != 'Y' and choice.upper() != 'N'):         #Play again ? 
        print('\tPLAY-AGAIN-? (Y/N)\n\t>>', end=' ') 
        choice = input() 
    if choice.upper() != 'Y': 
        game = False 

