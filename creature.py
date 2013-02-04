import main
from random import random

class State(object):
    # passive change should be a tuple of stats to modify and their change values
    #     eg ((0,-1), (2,1))
    # disable and reverse attack can either be TRUE or a lambda function
    #     eg lambda z : (random() < 0.5)
    def __init__(self, name, passiveChanges=None, disableAttack=None, reverseAttack=None):
        self._name = name
        self._passiveChanges = passiveChanges
        self._disableAttack = disableAttack
        self._reverseAttack = reverseAttack
        
    def Update(self, creature):
        if (self._passiveChanges==None):
            return
        for pc in self._passiveChanges:
            creature._currentStats[pc[0]] += pc[1]
    
    def IsAttackEnabled(self, lambdaInput=None):
        if (self._disableAttack == None):
            return True
        if (type(self._disableAttack) == type(False)):
            return not self._disableAttack
        else:
            return not self._disableAttack(lambdaInput)
    
    def IsAttackReverse(self, lambdaInput=None):
        if (self._reverseAttack == None):
            return False
        if (type(self._reverseAttack) == type(False)):
            return not self._reverseAttack
        else:
            return not self._reverseAttack(lambdaInput)
    
    def __repr__(self):
        return " --- Name: "+self._name+", passive: "+self._passiveChanges.__repr__()+", disable: "+self._disableAttack.__repr__()+" --- "
        
# attributes ["speed", "attack", "drunkeness", "defense", "levelingRate"]
POSSIBLE_STATES = {
    "poisoned": State("poisoned",[[2,-1]] ),
    "sleeping": State("sleeping",None,True),
    "frightened": State("frightened",None,True),
    "confused": State("confused",None,lambda z : (random() < 0.5),lambda z : (random() < 0.5)),
    "dead": State("dead",None,True)
    }

class Attack(object):
    # statesToAdd should be a State object or itterable of state objects
    # enemyStatChanges should be an itterable of stats to change, and by how much
    #     eg [[0,1], [2,-1]]
    def __init__(self, name, damage, recoil = 0, statesToAdd=None, stateChangeProbability = 0.2, critsAgainst = (), enemyStatChanges=None, enemyStatChangeProbability = 0, friendlyStatChanges=None):
        self._name = name
        self._damage = damage
        self._recoil = recoil
        self._statesToAdd = statesToAdd
        self._stateChangeProbability = stateChangeProbability
        self._critsAgainst = critsAgainst
        self._enemyStatChanges = enemyStatChanges
        self._enemyStatChangeProbability = enemyStatChangeProbability
        self._friendlyStatChanges = friendlyStatChanges

    @property
    def name(self):
        return self._name
        
    def Attack(self, attacker, deffender, playerAttack=False):
        # attributes ["speed", "damage", "drunkeness", "defense", "levelingRate"]
        story = []
        attacker.SetStat(2, attacker._currentStats[2]-self._recoil*attacker._currentStats[1])
        critDamage = 1.0
        if (random() > 0.95):
            critDamage *= 2.0
        if (self._critsAgainst):
            if (deffender._name in self._critsAgainst):
                critDamage *= 2.0

        if critDamage == 4.0:
            story.append('Super critical attack!!!!')
        elif critDamage == 2.0:
            story.append('Critical attack!')
                
        # attributes ["speed", "damage", "drunkeness", "defense", "levelingRate"]
        damage = self._damage*attacker._currentStats[1]*critDamage/deffender._currentStats[3]
        if damage <= deffender._attributes[2] * .1:
            story.append('Your attack is barley noticable.' if playerAttack else 'Your enemy attacks you, but you do not care.')
        elif damage > deffender._attributes[2] * .75:
            story.append('OMG DAMAGE AND STUFF')
        elif damage > deffender._attributes[2] * .5:
            story.append('Lots of damage')
        else:
            story.append('You actually do damage' if playerAttack else 'Your enemy is hurting you! Maybe you should actually care.')
        
        deffender.SetStat(2, deffender._currentStats[2]-damage)
        if (self._friendlyStatChanges):
            story.append('You do something to yourself, I\'m not sure what')
            for statChange in self._friendlyStatChanges:
                attacker.ModifyStat(statChange[0], statChange[1])
        if (self._enemyStatChanges):
            story.append('You do something to your enemy, I\'m not sure what')
            for statChange in self._enemyStatChanges:
                if (random() < self._enemyStatChangeProbability):
                    deffender.ModifyStat(statChange[0], statChange[1])
        if (self._statesToAdd):
            for stateChange in self._statesToAdd:
                if (random() < self._stateChangeProbability):
                    story.append('You change the enemies state!')
                    deffender.AddState(stateChange)
        return story
                
    def __repr__(self):
        return "\n<<<\n  ..attack "+self._name+"\n  ..damage "+self._damage.__repr__()+"\n  ..recoil "+self._recoil.__repr__()+"\n  ..states "+self._statesToAdd.__repr__()+"\n  ..probability "+self._stateChangeProbability.__repr__()+"\n  ..crits "+self._critsAgainst.__repr__()+"\n  ..enemy stat modifiers "+str(self._enemyStatChanges)+"\n  ..probability "+str(self._enemyStatChangeProbability)+"\n  ..friendly stat modifiers "+str(self._friendlyStatChanges)+"\n>>>"
    
ATTACKS = {
    "PassiveAgressiveStickyNotes": Attack("Passive Agressive Sticky Notes",2.0),
    "InsultYourCode": Attack("Insult Your Code",1.5,critsAgainst=("Programmer")),
    "UseStarTrekTrivia": Attack("Use Star Trek Trivia",1.0,0,[POSSIBLE_STATES["sleeping"]],0.6),
    "KickShins": Attack("Kick Shins",3.0,0.5,critsAgainst=("Dog")),
    "Bite": Attack("Bite",3.0),
    "Shoot": Attack("Shoot",4.0),
    "Taze": Attack("Taze",2.0),
    "Arrest": Attack("Arrest",3.0,critsAgainst=("Hooker")),
    "ChewBones": Attack("Chew Bones",2.0,critsAgainst=("Dog")),
    "GrowlMenacingly": Attack("Growl Menacingly",0,0,[POSSIBLE_STATES["frightened"]],0.4,None,[[1,-0.2]],1.0),
    "EatShoes": Attack("Eat Shoes",2.0,critsAgainst=("Programmer")),
    "StabWithAPoisonedNeedle": Attack("Stab With A Poisoned Knife",1.0,0,[POSSIBLE_STATES["poisoned"]],0.5),
    "StabWithShoe": Attack("Stab With A Stiletto Heel",4.0,0,[POSSIBLE_STATES["poisoned"]],0.3),
    "Strangle": Attack("Strangle",2.0,0,[POSSIBLE_STATES["sleeping"]],0.2),
	"EyeGouge": Attack("EyeGouge",3.0,0,[POSSIBLE_STATES["sleeping"]],0.3),
    "TapDance": Attack("Tap Dance",0.0,1.0,[POSSIBLE_STATES["confused"]],1.0),
    "OutrightKill": Attack("Outright Kill",99999),
    "SpreadFilth": Attack("Spread Filth",0.5,0.0,[POSSIBLE_STATES["poisoned"]],0.2),
	    # statesToAdd should be a State object or itterable of state objects
    # enemyStatChanges should be an itterable of stats to change, and by how much
    #     eg [[0,1], [2,-1]]
    #def __init__(self, name, damage, recoil = 0, statesToAdd=None, stateChangeProbability = 0.2, critsAgainst = (), enemyStatChanges=None, enemyStatChangeProbability = 0, friendlyStatChanges=None):
    }

# attributes ["speed", "attack", "drunkeness", "defense", "levelingRate"]
CREATURES = {
    "Programmer": {"attributes": [2.0, 0.5, 8.0, 1.0, 1.4],
                   "stateRecoveryRate": 2,
                   "attacks": (
            ATTACKS["PassiveAgressiveStickyNotes"],
            ATTACKS["InsultYourCode"],
            ATTACKS["UseStarTrekTrivia"],
            ATTACKS["KickShins"]
            ),

                   "attackLevels": [0, 0, 0, 0] },

    "Cockroach": {"attributes": [1.0, 0.1, 1.0, 1, 0.01],
                   "stateRecoveryRate": 2,
                   "attacks": (
            ATTACKS["GrowlMenacingly"],
            ATTACKS["Bite"],
            ATTACKS["SpreadFilth"],
            ATTACKS["EatShoes"]
            ),
                   "attackLevels": [0, 0, 0, 0] },

    "Rat": {"attributes": [1.5, 1.0, 2.0, 1, 1.1],
                   "stateRecoveryRate": 2,
                   "attacks": (
            ATTACKS["ChewBones"],
            ATTACKS["Bite"],
            ATTACKS["SpreadFilth"],
            ATTACKS["EatShoes"]
            ),
                   "attackLevels": [0, 0, 0, 0] },

    "Racoon": {"attributes": [2.0, 1.0, 2.0, 2, 1.5],
                   "stateRecoveryRate": 2,
                   "attacks": (
            ATTACKS["GrowlMenacingly"],
            ATTACKS["Bite"],
            ATTACKS["Strangle"],
            ATTACKS["EyeGouge"]
            ),
                   "attackLevels": [0, 0, 0, 0] },

    "Hooker": {"attributes": [6.0, 1.0, 2.0, 2, 1.5],
                   "stateRecoveryRate": 2,
                   "attacks": (
            ATTACKS["GrowlMenacingly"],
            ATTACKS["StabWithShoe"],
            ATTACKS["Strangle"],
            ATTACKS["EyeGouge"]
            ),
                   "attackLevels": [0, 0, 0, 0] },

    "HotCop": {"attributes": [8.0, 4.0, 2.0, 2, 1.5],
                   "stateRecoveryRate": 2,
                   "attacks": (
            ATTACKS["Shoot"],
            ATTACKS["Taze"],
            ATTACKS["Strangle"],
            ATTACKS["Arrest"]
            ),
                   "attackLevels": [0, 0, 0, 0] },

    "Poodle": {"attributes": [4.0, 2.0, 5.0, 1.1, 1.1],
            "stateRecoveryRate": 3,
            "attacks": (
            ATTACKS["Bite"],
            ATTACKS["ChewBones"],
            ATTACKS["GrowlMenacingly"],
            ATTACKS["EatShoes"]
            ),
            "attackLevels": [0, 0, 0, 0] }

    "Dog Walker": {"attributes": [5.0, 1.0, 2.0, 2, 1.5],
                   "stateRecoveryRate": 2,
                   "attacks": (
            ATTACKS["Tazer"],
            ATTACKS["Kick Shins"],
            ATTACKS["Strangle"],
            ATTACKS["EyeGouge"]
            ),
                   "attackLevels": [0, 0, 0, 0] },

    "Groundhog": {"attributes": [2.5, 2.0, 2.0, 1, 1.1],
                   "stateRecoveryRate": 2,
                   "attacks": (
            ATTACKS["ChewBones"],
            ATTACKS["Bite"],
            ATTACKS["GrowlMenacingly"],
            ATTACKS["EatShoes"]
            ),
                   "attackLevels": [0, 0, 0, 0] },

    "Dog": {"attributes": [3.0, 2.0, 5.0, 1.1, 1.1],
            "stateRecoveryRate": 3,
            "attacks": (
            ATTACKS["Bite"],
            ATTACKS["ChewBones"],
            ATTACKS["GrowlMenacingly"],
            ATTACKS["EatShoes"]
            ),
            "attackLevels": [0, 0, 0, 0] }
    }

class Creature(object):
    def __init__(self, creatureType):
        self._level = 0
        self._attributes = CREATURES[creatureType]["attributes"][:]
        self._currentStats = self._attributes[:]
        self._name = creatureType
        self._state = []
        self._stateRecoveryStages = {"normal":0,"poisoned":0,"sleeping":0,"frightened":0,"confused":0,"dead":0}
        self._stateRecoveryRate = CREATURES[creatureType]["stateRecoveryRate"]
        self._allAttacks = CREATURES[creatureType]["attacks"]
        self._attackLevels = CREATURES[creatureType]["attackLevels"]
        self._attacks = []
        self._autoAssignAttacks()
        self._streetCred = 0 # experience

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def health(self):
        return self._currentStats[2]

    @property
    def maxHealth(self):
        return self._attributes[2]

    @property
    def attacks(self):
        return self._attacks[:]
    
    """
    " Call this when the creature kills another creature
    " @deffender is the opponent creature (used to add streetCred)
    """
    def WinFight(self, deffender):
        nextLevel = ((self._level+1)**1.5)*10
        self._streetCred += deffender._level
        if (nextLevel <= self._streetCred):
            self.LevelUp()
    
    def LevelUp(self):
        self._level += 1
        currentLevel = (self._level**1.5)*10
        self._streetCred = max(self._streetCred, currentLevel)
        for i in range(len(self._attributes)-1):
            self._attributes[i] *= self._attributes[-1]
            self._currentStats[i] = self._attributes[i]

    """
    " adds the latest four attacks that the creature knows to the list of attacks
    """
    def _autoAssignAttacks(self):
        for x in range(len(self._allAttacks)):
            i = -(x+1)
            if (self._level >= self._attackLevels[i]):
                self._attacks.append(self._allAttacks[x])
                if (len(self._attacks) == 4):
                    return

    """
    " attack should be one of the attacks in self._attacks
    " deffender should be the other creature being fought
    """
    def Attack(self, attack, deffender, playerAttack=False):
        story = list()
        story.append('You use ' + attack.name + '.' if playerAttack else 'Your adversary uses ' + attack.name + '.')
        attackReversed = False
        for state in self._state:
            if (state._name == "dead"):
                return ['Already dead, BUG']
            if (not state.IsAttackEnabled()):
                return ['You have an existential crisis.'] if playerAttack else ['Your enemy has an existential crisis.']
            if (state.IsAttackReverse()):
                attackReversed = True
        if (not attackReversed):
            story += attack.Attack(self, deffender)
        else:
            story += ['You are an emo.'] + attack.Attack(self, self)
        self.IsDead()
        return story
        
    def SetStat(self, statIndex, value):
        if (self.IsDead()):
            return
        self._currentStats[statIndex] = value
    
    def ModifyStat(self, statIndex, value):
        if (self.IsDead()):
            return
        self._currentStats[statIndex] += value

    def AddState(self, state):
        for s in self._state:
            if (s == state or s._name == "dead"):
                return
        self._state.append(state)
        self._stateRecoveryStages[state._name] = 10
    
    def _Die(self):
        self._state = []
        self.AddState(POSSIBLE_STATES["dead"])
        self._stateRecoveryStages["dead"] = -1
    
    def IsDead(self):
        for state in self._state:
            if (state._name == "dead"):
                return True
        if (self._currentStats[2] <= 0):
            self._Die()
            return True
        return False
    
    """
    " percentDrunkeness is a float (0-1) of how much drunkeness the creature recovers
    """
    def Rececitate(self, percentDrunkeness):
        if (not self.IsDead()):
            return
        self._stateRecoveryStages["dead"] = 0
        for state in self._state:
            if (state._name == "dead"):
                self._state.remove(state)
                break
        self._currentStats[2] = self._attributes[2]*percentDrunkeness
    
    """
    " should be called once per round, just before this creature's turn
    " returns True if the creature dies
    " returns False otherwise, or the creature is already dead
    """
    def Update(self):
        removeFrom = []
        for state in self._state:
            if (state._name == "dead"):
                return False
            self._stateRecoveryStages[state._name] = max(0, self._stateRecoveryStages[state._name]-self._stateRecoveryRate)
            if (self._stateRecoveryStages[state._name] == 0):
                removeFrom.append(state)
            # check the states, specifically
            state.Update(self)
        for remove in removeFrom:
            self._state.remove(remove)
        return self.IsDead()
                
    def __repr__(self):
        return "..name "+self._name+"\n..level "+self._level.__repr__()+"\n..stats "+self._currentStats.__repr__()+"\n..max attrs "+self._attributes.__repr__()+"\n..states "+self._state.__repr__()+"\n..state stages: "+str(self._stateRecoveryStages)+"\n..recovery rate "+self._stateRecoveryRate.__repr__()+"\n..attacks "+self._attacks.__repr__()

if __name__ == "__main__":
    c = Creature("Programmer")
    print c
    c.LevelUp()
    print ""
    print c
    c.Attack(ATTACKS["OutrightKill"], c)
    c.Update()
    print ""
    print c
    c.Rececitate(0.5)
