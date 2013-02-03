import main
from random import random

class State(object):
    # passive change should be a tuple of stats to modify and their change values
    #     eg ((0,-1), (2,1))
    # disable attack can either be TRUE or a lambda function
    #     eg lambda z : (random() < 0.5)
    def __init__(self, name, passiveChanges=None, disableAttack=None):
        self._name = name
        self._passiveChange = passiveChange
        self._disableAttack = disableAttack
        
    def Update(self, creature):
        if (self._passiveChange==None):
            return
        for pc in self._passiveChanges:
            creature._currentStats[pc[0]] += pc[1]
    
    def IsAttackEnabled(self, lambdaInput=None):
        if (type(self._disableAttack) == type(False)):
            return self._disableAttack
        else:
            return self._disableAttack(lambdaInput)
        
# attributes ["speed", "damage", "drunkeness", "levelingRate"]
POSSIBLE_STATES = {
    "normal": State("normal"),
    "poisoned": State("poisoned",((2,-1)) ),
    "sleeping": State("sleeping",None,True),
    "frightened": State("frightened",None,True)
    }

class Attack(object):
    # stateToAdd should be a State object
    # statChanges should be a tuple of stats to change
    #     eg ((0,1), (2,-1))
    def __init__(self, name, damage, recoil = 0, stateToAdd=None, stateChangeProbability = 0.2, critsAgainst = (), statChanges=None, statChangeProbability = 0):
        self._damage = damage
        self._recoil = recoil
        self._stateToAdd = stateToAdd
        self._statChangeProbability = statChangeProbability
        self._critsAgainst = critsAgainst
        self._stateChange = stateChange
        self._stateChangeProbability = stateChangeProbability
        
    def Attack(self, attacker, deffender):
        attacker.SetStat("drunkeness", attacker.GetStat("drunkeness")-self._recoil*attacker.GetStat("damage"))
        critDamage = 1.0
        if (random() > 0.95):
            critDamage *= 2.0
        if (deffender.GetName in self._critsAgainst):
            critDamage *= 2.0
        deffender.setStat("drunkeness", deffender.GetStat("drunkeness")-self._damage*attacker.GetStat("damage")*critDamage)
        for statChange in self._statChange:
            if (random() < self._statChangeProbability):
                deffender.ModifyStat(statChange[0], statChange[1])
        for stateChange in self._stateChange:
            if (random() < self._stateChangeProbability):
                deffender.AddState(stateChange)

ATTACKS = {
    "PassiveAgressiveStickyNotes": Attack("Passive Agressive Sticky Notes",2.0),
    "InsultYourCode": Attack("Insult Your Code",1.5,critsAgainst=("Programmer")),
    "UseStarTrekTrivia": Attack("Use Star Trek Trivia",1.0,0,POSSIBLE_STATES["sleeping"],0.6),
    "KickShins": Attack("Kick Shins",3.0,0.5,critsAgainst=("Dog")),
    "Bite": Attack("Bite",3.0),
    "Chew Bones": Attack("Chew Bones",2.0,critsAgainst=("Dog")),
    "Growl Menacingly": Attack("Growl Menacingly",0,0,POSSIBLE_STATES["frightened"],0.4),
    "Eat Shoes": Attack("Eat Shoes",2.0,critsAgains=("Programmer"))
    }

# attributes ["speed", "damage", "drunkeness", "levelingRate"]
CREATURES = {
    "Programmer": {"attributes": (2.0, 0.5, 8.0, 1.4),
                   "stateRecoveryRate": 2,
                   "attacks": (
            ATTACKS("PassiveAgressiveStickyNotes"),
            ATTACKS("InsultYourCode"),
            ATTACKS("UseStarTrekTrivia"),
            ATTACKS("KickShins")
            ),
                   "attackLevels": (0, 0, 0, 0) },
    "Dog": {"attributes": (3.0, 2.0, 5.0, 1.1),
            "stateRecoveryRate": 3,
            "attacks": (
            Attack("Bite"),
            Attack("ChewBones"),
            Attack("GrowlMenacingly"),
            Attack("EatShoes")
            ),
            "attackLevels": (0, 0, 0, 0) }
    }

class Creature(object):
    def __init__(self, creatureType):
        # each action is a tuple (action name, damage multiplier)
        self._attributes = CREATURES[creatureType]["attributes"]
        self._currentStats = self._attributes
        self._name = creatureType
        self._state = set(["normal"])
        self._stateRecoveryStages = {"normal":0,"poisoned":0,"sleeping":0,"frightened":0}
        self._stateRecoveryRate = CREATURES[creatureType]["stateRecoveryRate"]
        self._allAttacks = CREATURES[creatureType]["attacks"]
        self._attackLevels = CREATURETYPE[creatureType]["attackLevels"]
        self._attacks = None
        self._autoAssignAttacks()
        self._level = 0

    """
    " adds the latest four attacks that the creature knows to the list of attacks
    """
    def _autoAssignAttacks(self):
        for x in range(len(self._allAttacks)):
            i = -(x+1)
            if (self._level >= self._attackLevels[i]):
                self._attacks.add(self._allAttacks[x])
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
        self._state.add(state)
        self._stateRecoveryStages[state._name] = 10
        
    """
    " should be called once per round, just before this creature's turn
    " returns True if the creature dies
    " returns False otherwise
    """
    def UpdateState(self):
        removeFrom = set()
        for state in self._states:
            self._stateRecoveryStages[stateName] = max(0, self._stateRecoveryStages[stateName]-self._stateRecoveryRate)
            if (self._stateRecoveryStages[stateName] == 0):
                removeFrom.add(state)
            # check the states, specifically
            state.Update(self)
        for remove in removeFrom:
            self._state.remove(remove)
        if (self._currentStats[2] == 0):
            self._die()
            return True
        return False

if __name__ == "__main__":
    c = Creature("Programmer")
