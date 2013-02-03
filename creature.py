import main
from random import random

class State(object):
    # passive change should be a tuple of stats to modify and their change values
    #     eg ((0,-1), (2,1))
    # disable attack can either be TRUE or a lambda function
    #     eg lambda z : (random() < 0.5)
    def __init__(self, name, passiveChanges=None, disableAttack=None):
        self._name = name
        self._passiveChanges = passiveChanges
        self._disableAttack = disableAttack
        
    def Update(self, creature):
        if (self._passiveChanges==None):
            return
        for pc in self._passiveChanges:
            creature._currentStats[pc[0]] += pc[1]
    
    def IsAttackEnabled(self, lambdaInput=None):
        if (type(self._disableAttack) == type(False)):
            return self._disableAttack
        else:
            return self._disableAttack(lambdaInput)
        
# attributes ["speed", "attack", "drunkeness", "defense", "levelingRate"]
POSSIBLE_STATES = {
    "poisoned": State("poisoned",((2,-1)) ),
    "sleeping": State("sleeping",None,True),
    "frightened": State("frightened",None,True)
    }

class Attack(object):
    # statesToAdd should be a State object or tuple of state objects
    # statChanges should be a tuple of stats to change
    #     eg ((0,1), (2,-1))
    def __init__(self, name, attack, recoil = 0, statesToAdd=None, stateChangeProbability = 0.2, critsAgainst = (), statChanges=None, statChangeProbability = 0):
        self._attack = attack
        self._recoil = recoil
        self._statesToAdd = statesToAdd
        self._stateChangeProbability = stateChangeProbability
        self._critsAgainst = critsAgainst
        self._statChanges = statChanges
        self._statChangeProbability = statChangeProbability
        
    def Attack(self, attacker, deffender):
        # attributes ["speed", "attack", "drunkeness", "defense", "levelingRate"]
        attacker.SetStat(2, attacker._currentStats[2]-self._recoil*attacker._currentStats[1])
        critDamage = 1.0
        if (random() > 0.95):
            critDamage *= 2.0
        if (deffender._name in self._critsAgainst):
            critDamage *= 2.0
        # attributes ["speed", "attack", "drunkeness", "defense", "levelingRate"]
        deffender.SetStat(2, deffender._currentStats[2]-self._attack*attacker._currentStats[1]*critDamage/deffender._currentStats[3])
        if (self._statChanges):
            for statChange in self._statChanges:
                if (random() < self._statChangeProbability):
                    deffender.ModifyStat(statChange[0], statChange[1])
        if (self._statesToAdd):
            for stateChange in self._statesToAdd:
                if (random() < self._stateChangeProbability):
                    deffender.AddState(stateChange)
                
    def __repr__(self):
        return ["attack "+self._attack.__repr__(), "recoil "+self._recoil.__repr__(), "states "+self._statesToAdd.__repr__(), "probability "+self._stateChangeProbability.__repr__(), "crits "+self._critsAgainst.__repr__(), "stats "+self._statChanges.__repr__(), "probability "+self._statChangeProbability.__repr__()].__repr__();
    
ATTACKS = {
    "PassiveAgressiveStickyNotes": Attack("Passive Agressive Sticky Notes",2.0),
    "InsultYourCode": Attack("Insult Your Code",1.5,critsAgainst=("Programmer")),
    "UseStarTrekTrivia": Attack("Use Star Trek Trivia",1.0,0,POSSIBLE_STATES["sleeping"],0.6),
    "KickShins": Attack("Kick Shins",3.0,0.5,critsAgainst=("Dog")),
    "Bite": Attack("Bite",3.0),
    "ChewBones": Attack("Chew Bones",2.0,critsAgainst=("Dog")),
    "GrowlMenacingly": Attack("Growl Menacingly",0,0,POSSIBLE_STATES["frightened"],0.4),
    "EatShoes": Attack("Eat Shoes",2.0,critsAgainst=("Programmer"))
    }

# attributes ["speed", "attack", "drunkeness", "defense", "levelingRate"]
CREATURES = {
    "Programmer": {"attributes": [2.0, 0.5, 8.0, 1.2, 1.4],
                   "stateRecoveryRate": 2,
                   "attacks": (
            ATTACKS["PassiveAgressiveStickyNotes"],
            ATTACKS["InsultYourCode"],
            ATTACKS["UseStarTrekTrivia"],
            ATTACKS["KickShins"]
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
        self._attributes = CREATURES[creatureType]["attributes"]
        self._currentStats = self._attributes
        self._name = creatureType
        self._state = []
        self._stateRecoveryStages = {"normal":0,"poisoned":0,"sleeping":0,"frightened":0}
        self._stateRecoveryRate = CREATURES[creatureType]["stateRecoveryRate"]
        self._allAttacks = CREATURES[creatureType]["attacks"]
        self._attackLevels = CREATURES[creatureType]["attackLevels"]
        self._attacks = []
        self._autoAssignAttacks()

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
    """
    def Attack(self, attack, deffender):
        for state in self._state:
            if (not state.IsAttackEnabled()):
                return
        attack.Attack(self, deffender)
        
    def SetStat(self, statIndex, value):
        self._currentStats[statIndex] = value
    
    def ModifyStat(self, statIndex, value):
        self._currentStats[statIndex] += value

    def AddState(self, state):
        if (state in self._state):
            return
        self._state.append(state)
        self._stateRecoveryStages[state._name] = 10
        
    """
    " should be called once per round, just before this creature's turn
    " returns True if the creature dies
    " returns False otherwise
    """
    def UpdateState(self):
        removeFrom = []
        for state in self._states:
            self._stateRecoveryStages[stateName] = max(0, self._stateRecoveryStages[stateName]-self._stateRecoveryRate)
            if (self._stateRecoveryStages[stateName] == 0):
                removeFrom.append(state)
            # check the states, specifically
            state.Update(self)
        for remove in removeFrom:
            self._state.remove(remove)
        if (self._currentStats[2] == 0):
            self._die()
            return True
        return False
                
    def __repr__(self):
        return ["name "+self._name, "level "+self._level.__repr__(), "stats "+self._currentStats.__repr__(), "max attrs "+self._attributes.__repr__(), "states "+self._state.__repr__(), "recovery rates "+self._stateRecoveryRate.__repr__(), "attacks "+self._attacks.__repr__()].__repr__()

if __name__ == "__main__":
    c = Creature("Programmer")
    print c
    c.Attack(c._attacks[0], c)
    print ""
    print c
