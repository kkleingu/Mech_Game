import random, os, math, time


############ Functions ##############
          
def cls(): 
    if os.system("clear") == 1: 
        os.system("cls") 
    else: 
        os.system("clear") 

def legalMove(grid, unit, combatants, move):
    potentialLocation = (unit.location[0] + move[0],unit.location[1] + move[1])
    others = list(combatants)
    others.remove(unit)
    otherlocations = []
    gridy = len(grid)-1
    gridx = len(grid[0])-1
    
    for i in others:
        otherlocations.append(i.location)
    if potentialLocation[0] > gridx or potentialLocation[0] < 0 or potentialLocation[1] > gridy or potentialLocation[1] < 0  : #Outside of borders
        return False
    elif potentialLocation in otherlocations: #Another Unit is already in that location
        return False
    else:
        return True
        
def victoryCondition(combatants):
    names = []
    for unit in combatants:
        names.append(unit.name)
    if len(combatants) == 1:
        if combatants[0].name == 'User':
            print('PLAYER WINS')
            input()
            return False
        else:
            print('PLAYER LOSES')
            input()
            return False
    elif 'User' not in names:
        print('PLAYER DEAD\n PLAYER LOSES')
        return False           
    else:
        return True
    
######### Map Functions ##############

def printMap(grid, combatants):         #Prints the map 
    print('UNITS:')
    for unit in combatants:
        print('\t[ %s ]\t/ %s /  TEAM  %s  /  HEALTH  %d' % (unit.symbol, unit.name, unit.team, unit.health)) 

    for i in range(len(grid)): 
        print('', end='\t') 
        for j in range(len(grid[i])): 
            print(grid[i][j], end=' ') 
        print('')
        
def placeUnits(grid, combatants):                      #Updates the unit's placement 
    for i in combatants:
        grid[i.location[0]][i.location[1]] = i.symbol

def blankGrid(grid):                        #Clears the grid, preaparing it for updates 
    for i in range(len(grid)): 
        for j in range(len(grid[i])): 
            grid [i][j] = '.' 
    return grid

def updateMap(grid, combatants):
    cls()
    grid = blankGrid(grid) ### Resets the grid to original (Maybe Save the default grid if we modify it later with hills etc)
    placeUnits(grid, combatants) ##### Places Units onto grid
    printMap(grid,combatants)

######### Movement Functions #######3


def playerTurn(unit, movements, combatants, grid):#Player's turn
    Attacked = False
    while True and not Attacked:                         #Keeps asking input until its valid 
        print('\nMOVE OPTIONS:\n\t[*]UP\t/ W\n\t[*]DOWN\t/ S\n\t[*]LEFT\t/ A\n\t[*]RIGHT/ D\n\t[*]STOP\t/ Q\n\t[*]FIRE\t/ SPACE\n\t[*]INTEL/ I\n\n\t\t>>', end=' ') 
        playerMove = input()

        if playerMove.upper() in movements:
            if legalMove(grid, unit, combatants, movements[playerMove.upper()]):
                unit.Move(movements[playerMove.upper()])
                break
            else:
                print('Illegal Move')
                input()
                updateMap(grid, combatants)
                    
        if  playerMove.upper() == ' ':   #### Firing Command ####
            Attacking = True
            while Attacking:
                weaponselected = False
                targetselected = False
                while not targetselected:
                    print('WHICH ENEMY?:')
                    enemies = list(combatants)
                    enemies.remove(unit)
                    for enemy in range(len(enemies)):
                        print('\t[',enemy,']', " '",enemies[enemy].symbol,"'  / ",enemies[enemy].name,' /  DISTANCE', unit.weaponDistance(enemies[enemy]),' /  TEAM',enemies[enemy].team,) 
                    print('\t[ B ] \t/ BACK')  #####Need to implement a back button
                    enemyAttack = input()

                    try:  ######## Working on a back button so you arent locked in
                        if enemyAttack.upper() == 'B':
                            updateMap(grid, combatants)
                            Attacking = False
                            break
                    except ValueError:
                        pass

                    try:
                        enemyAttack = int(enemyAttack)
                        if enemyAttack in range(len(enemies)): ###### Check if values are good ######
                            targetselected = True
                            break
                    except ValueError:
                        pass
                if not Attacking: #### Means someone said back
                    break
                
                while not weaponselected:    
                    print('WHICH WEAPON?')
                    for weapon in range(len(unit.weapons)): ####Weapon list
                        print('\t[',weapon,'] %s' % unit.weapons[weapon].getIntel())   
                    print('\t[ B ] \t/ BACK')    
                    weaponAttack = input()
                    
                    try:  
                        if weaponAttack.upper() == 'B':
                            updateMap(grid, combatants)
                            targetselected = False
                            break
                    except ValueError:
                        pass

                    try:
                        weaponAttack = int(weaponAttack)
                        if weaponAttack in range(len(unit.weapons)): ###### Check if values are good ######
                            weaponselected = True
                            break
                    except ValueError:
                        pass
                if weaponselected:
                    unit.Attack(enemies[enemyAttack], weaponAttack)
                    input()
                    Attacking = False
                    Attacked = True

        if  playerMove.upper() == 'I':
            while True:
                print('SELECT A MECH FOR INTEL')
                for u in range(len(combatants)):
                    print('\t[',u,']', " '",combatants[u].symbol,"'  / ",combatants[u].name) 
                intel = input()
                try:
                    intel = int(intel)
                    if intel in range(len(combatants)): ###### Check if values are good ######
                        combatants[intel].getIntel(unit)
                        input()
                        updateMap(grid, combatants)
                        break
                except ValueError:
                    
                    pass

def computerTurn(unit, movements, combatants, grid):           #Computers turn get within a space and shoot? 
    allies, enemies = unit.getAllies(list(combatants))
    ##### Find Closest Enemy to engage #####
    enemydistances = []
    for u in enemies:
        enemydistances.append(unit.weaponDistance(u))
    enemy = enemies[enemydistances.index(min(enemydistances))]
    if unit.weaponDistance(enemy) <= 1:
        unit.Attack(enemy, 0) #### Attacks the user with a laser
        
    else: ##### Not within 1 aka range gets closer (Could shoot from father away)  Maybe make a second personality that doe
        distance = unit.coordinateDistance(enemy)
        if abs(distance[0]) > abs(distance[1]):
            priority = 0 ### Priority is move in y axis
            secondary = 1
        else:
            priority = 1 ### Priority is move in x axis
            secondary = 0
        potentialmoves = []
        if distance[0] == 0: ###Error if you divide by 0
            potentialmoves.append((0,0))
        else:
            potentialmoves.append((int(distance[0]/abs(distance[0])) * -1 , 0)) # Negative bc (0,0) is top left and not bottom left of grid
        if distance[1] == 0: ###Error if you divide by 0
            potentialmoves.append((0,0))
        else:
            potentialmoves.append((0,int(distance[1]/abs(distance[1]))*-1))

        if legalMove(grid, unit, combatants, potentialmoves[priority]):
            unit.Move(potentialmoves[priority])

        elif legalMove(grid, unit, combatants, potentialmoves[secondary]):
            unit.Move(potentialmoves[secondary])

        else:
            unit.Move((0,0)) #Doesn't move
    time.sleep(2)
        
