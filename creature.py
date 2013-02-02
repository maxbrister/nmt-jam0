import main
import random from random

class Attack(object):
    def __init__(self, damage, recoil, statChange = -1, statChangeProbability = 0.2, critsAgainst = ()):
        self._damage = damage
        self._recoil = recoil
        self._statChange = statChange
        self._statChangeProbability = statChangeProbability
        self._critsAgainst = critsAgainst
        
    def Attack(self, attacker, deffender):
        attacker.SetStat("drunkeness", attacker.GetStat("drunkeness")-self._recoil*attacker.GetStat("damage"))
        critDamage = 1.0
        if (random() > 0.95):
            critDamage *= 2.0
        if (deffender.GetName in self._critsAgainst):
            critDamage *= 2.0
        deffender.setStat("drunkeness", deffender.GetStat("drunkeness")-self._damage*attacker.GetStat("damage")*critDamage)
        if (statChange != -1):
            if (random() < statChangeProbability):
                deffender.setState(statChange)


ATTRIBUTE_NAME_TO_VALUE = ["speed", "damage", "drunkeness", "levelingRate"]
CREATURES = {
    "Programmer": {"attributes": (2.0, 0.5, 8.0, 1.4),
                   "stateRecoveryRate": 2,
                   "attacks": ("Passive Agressive Sticky Notes", "Insult Your Code", "Use Star Trek Trivia", "Kick Shins"),
                   "attackLevels": (0, 0, 0, 0) }
    "Dog": {"attributes": (3.0, 2.0, 5.0, 1.1),
            "stateRecoveryRate": 3,
            "attacks": ("Bite", "Chew Bones", "Growl Menacingly", "Eat Shoes"),
            "attackLevels": (0, 0, 0, 0) }
    }

class Creature(object):
    def __init__(self, creatureType):
        # each action is a tuple (action name, damage multiplier)
        self._attributes = CREATURES[creatureType]["attributes"]
        self._currentStats = self._attributes
        self._name = creatureType
        self._state = set(["normal"])
        self._stateRecoveryStages = {"normal":0,"poisoned":0,"sleeping":0}
        self._stateRecoveryRate = CREATURES[creatureType]["stateRecoveryRate"]
        
    def GetStat(self, statName):
        return self._currentStats[statName]

    def GetName(self):
        return self._name
    
    def SetStat(self, statName, value):
        self._currentStats[statName] = value

    def SetState(self, stateName):
        self._state.add(stateName)
        self._stateRecoveryStages[stateName] = 10
        
    def GetState(self):
        return self._state

    def UpdateState(self):
        removeFrom = set()
        for state in self._state:
            self._stateRecoveryStages[stateName] = max(0, self._stateRecoveryStages[stateName]-self._stateRecoveryRate)
            if (self._stateRecoveryStages[stateName] == 0):
                removeFrom.add(state)
        for remove in removeFrom:
            self._state.remove(remove)
