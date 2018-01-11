import random, os, math, time


############### Classes ################
class Weapon:
    def getIntel(self):
        return ('%s \t/ DAMAGE  %d \t/  RANGE %d\t/  ACCURACY %.2f' % (self.name, self.damage, self.range, self.accuracy))

class Laser(Weapon):
    def __init__(self):
        self.name = 'LASER'
        self.range = 2
        self.damage = 4
        self.ammo = 10000
        self.heat = 10
        self.accuracy = 0.8

class LRM(Weapon):
    def __init__(self):
        self.name = 'LRM'
        self.range = 6
        self.damage = 2
        self.ammo = 10000
        self.heat = 10
        self.accuracy = 0.95



class Mech:
    def __init__(self, name, health, speed = 3, location = (0,0), symbol = 'X', \
                 weapons = [Laser()], team = None):
        ### Need to change symbol
        ## Eventually Add Pilot with dodging and gunnery skills as a seperate class
        self.name = name
        self.health = health
        self.speed = speed
        self.location = location
        self.symbol = symbol
        self.weapons = weapons
        self.mechtype = 'UNKNOWN'
        if team == None:
            self.team = None
        else:
            self.team = str(team).upper() ### Always Upper case

    def takeDamage(self, dmgAmount):
        self.health = self.health - dmgAmount
        if self.health <= 0:
            #print(self.name + ' IS DESTROYED!')
            return True #### It is destroyed
        else:
            #print(self.name + ' HAS %d HEALTH' % self.health)
            return False #### It is destroyed
        #elif self.health <10 and self.speed > 1:  ####Maybe at 50% but need to save the initial speed etc.
            #print(self.name + ' has leg damage!')

    def Move(self, movement):
        self.location = (self.location[0] + movement[0],self.location[1] + movement[1])

    def Attack(self, enemy, weaponnumber):
        if self.weaponDistance(enemy) <= self.weapons[weaponnumber].range:
            hitChance = math.pow(self.weapons[weaponnumber].accuracy, self.weaponDistance(enemy)) # =(Weapon Accuracy) ^ Distance
            if random.random() <= hitChance:
                enemy.takeDamage(self.weapons[weaponnumber].damage)
                if enemy.health <= 0:
                    return (str(self.name) +' destroyed ' + str(enemy.name))
                else:
                    return (str(enemy.name) + ' has ' + str(enemy.health) + ' health')
            else:
                return (str(self.name) + ' missed ' + str(enemy.name))
        else:
            return 'MISS DUE TO RANGE'

    def weaponsList(self):#### Making make and return a list instead of just printing
        for i in self.weapons:
            print(i.getIntel())

    def getIntel(self, other):
        print("' %s '\t/ %s \t/ CLASS %s  \t/ TEAM %s \t/ HEALTH %d \t/ SPEED %d \t/ DISTANCE %d"% (self.symbol, self.name, self.mechtype, self.team, self.health, self.speed, self.weaponDistance(other)))
        self.weaponsList()

    def coordinateDistance(self, enemy):
        coordinatedistance = (self.location[0] - enemy.location[0],self.location[1] - enemy.location[1])
        return coordinatedistance

    def weaponDistance(self, enemy):
        weapondistance = abs(self.location[0] - enemy.location[0]) + abs(self.location[1] - enemy.location[1])
        return weapondistance

    def addTeam(self, team):
        if team == None:
            self.team = None
        else:
            self.team = str(team).upper()

    def getAllies(self, combatants):
        potentialteam = list(combatants)
        potentialteam.remove(self)
        if self.team == None:
            self.allies = [self]
            self.enemies = potentialteam
        else:
            self.allies = [self]
            self.enemies = []
            for unit in potentialteam:
                if unit.team == self.team:
                    self.allies.append(unit)
                else:
                    self.enemies.append(unit)
        return self.allies, self.enemies


class Cricket(Mech):
    def __init__(self, name, location = (0,0), symbol = 'X', team = None):
        self.name = name
        self.health = 8
        self.speed = 3
        self.location = location
        self.symbol = symbol
        self.weapons = [Laser()]
        self.mechtype = 'CRICKET'
        if team == None:
            self.team = None
        else:
            self.team = str(team).upper() ### Always Upper case

class Gladiator(Mech):
    def __init__(self, name, location = (0,0), symbol = 'X', team = None):
        self.name = name
        self.health = 20
        self.speed = 3
        self.location = location
        self.symbol = symbol
        self.weapons = [Laser(), LRM()]
        self.mechtype = 'GLADIATOR'
        if team == None:
            self.team = None
        else:
            self.team = str(team).upper()

class Team:
    def __init__(self, name, TeamMembers = []):
        self.name = str(name).upper()
        self.teammembers = TeamMembers
        for member in self.teammembers:
            member.addTeam(self.name)
            member.allies = self.teammembers

    def addTeamMember(self, NewRecruit):
        self.teammembers.append(NewRecruit)
        NewRecruit.addTeam(self.name)
        for member in self.teammembers:
            member.allies.append(NewRecruit)

    def removeTeamMember(self, FormerRecruit):
        self.teammembers.remove(FormerRecruit)
        NewRecruit.addTeam(None)
        for member in self.teammembers:
            member.allies.remove(FormerRecruit)
