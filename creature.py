import collections
import main
import math
from random import random

class State(object):
    # passive change should be a tuple of stats to modify and their change values
    #     eg ((0,-1), (2,1))
    # disable and reverse attack can either be TRUE or a lambda function
    #     eg lambda z : (random() < 0.5)
    def __init__(self, name, appliedMessage, recoverMessage, passiveChanges=None, disableAttack=None,
                 reverseAttack=None):
        self._name = name
        self.appliedMessage = appliedMessage
        self.recoverMessage = recoverMessage
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
    "poisoned": State("poisoned",'{0} is poisoned.','{0} is cured of poison.',[[2,-1]]),
    "sleeping": State("sleeping",'{0} is sleeping.','{0} has woken up.',None,True),
    "frightened": State("frightened",'{0} is a scaredy-cat.','{0} is no longer frightened.',None,True),
    "confused": State("confused",'{0} is clueless','{0} had some sense knocked into him.',None,lambda z : (random() < 0.5),lambda z : (random() < 0.5)),
    "dead": State("dead",'{0} is dead as a door knob','{0} came back from the dead.',None,True)
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

    def Attack(self, attacker, defender, playerAttack=False):
        return [msg for msg in self.AttackGenerator(attacker, defender, playerAttack)]

    ''' Just like Attack, but generates the story on the fly. '''
    def AttackGenerator(self, attacker, defender, playerAttack=False):
        def DoProcessMessage(playerAttack, msgList):
            return msgList[0] if playerAttack else msgList[1]
        P = lambda msgPlayer, msgOpponent: DoProcessMessage(playerAttack, (msgPlayer, msgOpponent))
        
        critDamage = 1.0
        didCrit = random() > 0.95
        if didCrit:
            critDamage *= 2.0
        effective = False
        if (self._critsAgainst):
            if (defender._name in self._critsAgainst):
                effective = True
                critDamage *= 2.0
                
        # attributes ["speed", "damage", "drunkeness", "defense", "levelingRate"]
        damage = self._damage*attacker._currentStats[1]*critDamage/defender._currentStats[3]
        defender.SetStat(2, defender._currentStats[2]-damage)

        if effective:
            yield 'The attack is super effective!'

        if didCrit:
            yield 'Critical hit!'

        if damage <= defender._attributes[2] * .1:
            yield 'My grandma hits harder than that.'
        elif damage > defender._attributes[2] * .75:
            yield 'OMG DAMAGE AND STUFF!!!111!!'
        elif damage > defender._attributes[2] * .5:
            yield 'Lots of damage.'
        else:
            yield 'So-so damage.'
        
        if (self._friendlyStatChanges):
            for statChange in self._friendlyStatChanges:
                attacker.ModifyStat(statChange[0], statChange[1])
                yield self._StatsMessage(statChange, attacker, playerAttack)
        if (self._enemyStatChanges):
            for statChange in self._enemyStatChanges:
                if (random() < self._enemyStatChangeProbability):
                    defender.ModifyStat(statChange[0], statChange[1])
                    yield self._StatsMessage(statChange, attacker, not playerAttack)
        if (self._statesToAdd):
            for stateChange in self._statesToAdd:
                if (random() < self._stateChangeProbability):
                    defender.AddState(stateChange)
                    yield '{0} has been {1}.'.format(defender._name, stateChange._name)

        # attributes ["speed", "damage", "drunkeness", "defense", "levelingRate"]
        recoilAmt = self._recoil*attacker._currentStats[1]
        if recoilAmt > 0:
            yield '{0} take damage from the attack\'s recoil'.format(attacker._name)
        elif recoilAmt < 0:
            yield '{0} is healed by his deviant actions.'.format(attacker._name)
        attacker.SetStat(2, attacker._currentStats[2]-recoilAmt)

    def _StatsMessage(self, (stat, change), creature, isPlayer):
        msgBad = ['has been slowed', 'took extra damage', 'has had too much liquor',
                  'is rendered less able to defend', 'gets a little stupider']
        msgGood = ['looks like it is on caffeine', 'looks a little healtier', 'is starting to sober up',
                   'might be able to block a blow', 'looks a little smarter']
        if isPlayer:
            noun = 'Your'
        else:
            noun = 'Your opponent\'s'
        if change < 0:
            msg = msgBad
        else:
            msg = msgGood
        return '{0} {1} {2}.'.format(noun, msg[stat], creature._name)
                
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
    "SpreadFilth": Attack("Spread Filth",0.5,0.0,critsAgainst="Cop"),
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
            "attackLevels": [0, 0, 0, 0] },

    "Dog Walker": {"attributes": [5.0, 1.0, 2.0, 2, 1.5],
                   "stateRecoveryRate": 2,
                   "attacks": (
            ATTACKS["Taze"],
            ATTACKS["KickShins"],
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
    def speed(self):
        return self._currentStats[0]
    
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
    " @defender is the opponent creature (used to add streetCred)
    """
    def WinFight(self, defender):
        nextLevel = ((self._level+1)**1.5)*10
        self._streetCred += defender._level
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
    " defender should be the other creature being fought
    "
    " return - A list of strings which represent the attack story
    """
    def Attack(self, attack, defender, playerAttack=False):
        return [v for v in self.AttackGenerator(attack, defender, playerAttack)]


    '''
    Like Attack, but yields the story as the attack is in progress.
    '''
    def AttackGenerator(self, attack, defender, playerAttack=False):
        def DoProcessMessage(playerAttack, msgList):
            return msgList[0] if playerAttack else msgList[1]
        P = lambda msgPlayer, msgOpponent: DoProcessMessage(playerAttack, (msgPlayer, msgOpponent))

        yield P('Your {0} uses {1}.', 'Your oponent\'s {0} uses {1}.').format(self._name, attack.name)
            
        if random() <= 0.2:
            yield 'The attack fails!'
            return

        attackReversed = False
        for state in self._state:
            if (state._name == "dead"):
                yield 'Already dead, BUG'
                return
            
            if (not state.IsAttackEnabled()):
                yield 'The attack fails.'
                return
            if (state.IsAttackReverse()):
                attackReversed = True

        lhs = self
        if (not attackReversed):
            rhs = defender
        else:
            rhs = self
            yield '{0} is an emo.'.format(self._name)
            yield '{0} uses {1} on itself!'.format(self._name, attack.name)

        for msg in attack.AttackGenerator(lhs, rhs, playerAttack):
            yield msg
    
        
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

    def Update(self):
        [msg for msg in self.UpdateGenerator() if False]
        return self.IsDead()
    
    """
    " should be called once per round, just before this creature's turn
    """
    def UpdateGenerator(self):
        removeFrom = []
        for state in self._state:
            if (state._name == "dead"):
                return
            yield state.appliedMessage.format(self._name)
            self._stateRecoveryStages[state._name] = max(0, self._stateRecoveryStages[state._name]-self._stateRecoveryRate)
            if (self._stateRecoveryStages[state._name] == 0):
                removeFrom.append(state)
                yield state.recoverMessage.format(self._name)
            # check the states, specifically
            state.Update(self)

            # TODO: generalize this
            if state._name == 'poisoned':
                yield '{0} takes damage from the poison.'.format(state.name)
            
        for remove in removeFrom:
            self._state.remove(remove)
                
    def __repr__(self):
        return "..name "+self._name+"\n..level "+self._level.__repr__()+"\n..stats "+self._currentStats.__repr__()+"\n..max attrs "+self._attributes.__repr__()+"\n..states "+self._state.__repr__()+"\n..state stages: "+str(self._stateRecoveryStages)+"\n..recovery rate "+self._stateRecoveryRate.__repr__()+"\n..attacks "+self._attacks.__repr__()

def MakeCreatureMenu(player, onSelect, filterfn = lambda c: True):
    options = collections.OrderedDict()
    fmt = '{0} lvl: {1} health: {2}%'
    for idx, c in enumerate(player.creatures):
        if filterfn(c):
            if c.IsDead():
                name = fmt.format(c.name, c.level, 'DEAD')
            else:
                name = fmt.format(c.name, c.level,
                                  max(1, int(math.floor(100 * float(c.health / c.maxHealth)))))
            options[name] = lambda idx=idx, c=c: onSelect(idx, c)
    return options

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
