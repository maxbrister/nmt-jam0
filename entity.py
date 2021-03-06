import collections
import gametime
import graphics
import numpy

from gametime import GameTime
from graphics import Sprite
from creature import Creature
from copy import deepcopy
from random import random, randint, seed
from time import time
seed(time())

"""
" The entity class should be used for anything that has a sprite, position, and can interact with other entities.
" Entities have the movement methods StartMovement, IsMoving, and Move. For immobile entities (such as a flower pot), use the ImmobileEntity class.
" The interact method is an abstract method, meant to be implemented more in later classes.
"""

class Entity(object):
    DIRECTION_TO_ANIM = ['n', 'e', 's', 'w']
    DIRECTION_TO_DELTA = numpy.array([(0,-1), (1,0), (0,1), (-1,0)])
    
    """
    " @spriteName the graphical representation of the Entity
    " @Position a numpy.array
    " @gameBoard the gameboard object
    " @secondsToMove the number of seconds it should take to finish the animated movement
    """
    def __init__(self, spriteName, position, gameBoard, secondsToMove=0.4):
        self._sprite = Sprite(spriteName)
        self._position = numpy.array(position)
        self._oldPosition = self._position.copy()
        self._movingState = "notMoving" # a string ("notMoving", "starting", "movingOut", "movingIn" "finishing")
        self._movingFrame = 0 # an integer, starting with 0 for before the first moving query from the game loop
        self._movingStartTime = GameTime()
        self._gameBoard = gameBoard
        self._secondsToMove = secondsToMove
        self._sprite.position = self._position * gameBoard.tileSize
        self._movingDirection = 4 # stoped
        self._renderDirection = Entity.DIRECTION_TO_ANIM[1] # direction to render if stoped (last direction)
        
        #dictionary of dialogue texts keyed by plot events
        self.dialogueList = collections.OrderedDict()
        self._hasDialogue = False
        
        gameBoard.Add(self, position)

    @property
    def drawPosition(self):
        return numpy.array(self._sprite.position, dtype=numpy.double)

    @property
    def targetPosition(self):
        if self._movingState in ['starting', 'movingOut']:
            return self._position + Entity.DIRECTION_TO_DELTA[self._movingDirection]
        return self._position.copy()

    @property
    def position(self):
        return self._position.copy()
    
    def Interact(self, entity):
        pass

    #add a named plot event with dialogue text to this npc
    def AddToDialogueList(self, plotEvent, dialogueTextList, endFunction = lambda player, npc: None):
        if isinstance(dialogueTextList, str):
            dialogueTextList = [dialogueTextList]
        self.dialogueList[plotEvent] = dialogueTextList, endFunction
        self._endFunction = endFunction

    def FinishDialouge(self, plotEvent, endFunction):
        textList, endFunction2 = self.dialogueList[plotEvent]
        def UnionFunction(player, npc, a, b):
            a(player, npc)
            return b(player, npc)
        self.AddToDialogueList(plotEvent, textList, lambda player, npc, a=endFunction2, b=endFunction: UnionFunction(player, npc, a, b))
    
    def RemoveFirstDialogue(self):
        self.dialogueList.popitem(False)
        if (len(self.dialogueList) == 0):
            self._hasDialogue = False
    
    """
    " Tells an entity to move one space toward the given direction
    " Can be 0, 1, 2, 3 or can be "up", "right", "down", "left"
    """
    def StartMovement(self, direction):
        if (self.IsMoving()):
            return
        d = self.TranslateDirection(direction)
        self._movingFrame = 0
        self._movingState = "starting"
        self._movingDirection = d
        self._movingStartTime = GameTime()
        self._renderDirection = Entity.DIRECTION_TO_ANIM[self._movingDirection] 

    """
    " Used by the game loop to determine if the entity is moving or not
    """
    def IsMoving(self):
        if (self._movingState == "notMoving" or self._movingState == "finishing"):
            return False
        return True

    def Render(self, ctx):
        if self._movingDirection < len(Entity.DIRECTION_TO_ANIM):
            self._renderDirection = Entity.DIRECTION_TO_ANIM[self._movingDirection] 
        self._sprite.SetFrame(self._renderDirection, self._movingFrame)
        self._sprite.Render(ctx)

    """
    " Stops the movement of the entity and resets its movement data
    """
    def StopMovement(self):
        self._movingState = "notMoving"
        self._movingFrame = 0
        self._movingDirection = 4 # stoped

    def Remove(self):
        self._gameBoard.Remove(self, self._position)

    """
    " Actually moves the object
    " Don't call this from outside the entity (treat it as a private method)
    """
    def _Move(self):
        self._movingState = "movingIn"
        self._oldPosition = self._position.copy()
        destination = self._position + Entity.DIRECTION_TO_DELTA[self._movingDirection]
        if (tuple(destination) in self._gameBoard.Movable(self._position)):
            # check that the destination is clear
            self._position += Entity.DIRECTION_TO_DELTA[self._movingDirection]
        self._gameBoard.Move(self, self._oldPosition, self._position)

    def Move(self):
        if (self._movingState == "finishing" or self._movingState == "notMoving"):
            self.StopMovement()
            self._sprite.position = self._position * self._gameBoard.tileSize
            return
            
        # update the state and frame
        self._movingFrame += 1
        percentDone = min(1.0, float(GameTime()-self._movingStartTime)/self._secondsToMove)
        if (percentDone >= 0.5 and (self._movingState == "movingOut" or self._movingState == "starting")):
            self._Move()
        if (percentDone >= 1.0):
            self._movingState = "finishing"

        # get the position as a float value (for drawing)
        source = numpy.array(self._position, dtype=numpy.double)
        dest = source.copy()
        if (self._movingState == "movingOut" or self._movingState == "starting"):
            # moving out of the current space (happens before the middle frame)
            dest += Entity.DIRECTION_TO_DELTA[self._movingDirection]
        elif (self._movingState == "movingIn"):
            # moving into the next space (happens after the middle frame
            if (self._oldPosition == self._position).all():
                source += Entity.DIRECTION_TO_DELTA[self._movingDirection]
            else:
                source -= Entity.DIRECTION_TO_DELTA[self._movingDirection]
        self._sprite.position = numpy.array(self._position, dtype=numpy.double)
        if (percentDone != 0.0):
            self._sprite.position = source+(dest-source)*percentDone
        self._sprite.position *= self._gameBoard.tileSize

    """
    " translate a direction string into an integer
    " Returns 0-3 for up, right, down, left
    " Returns -1 if none of the others are found
    """
    def TranslateDirection(self, direction):
        direction = direction.lower()
        if (direction == "up" or direction == 0):
            return 0
        if (direction == "right" or direction == 1):
            return 1
        if (direction == "down" or direction == 2):
            return 2
        if (direction == "left" or direction == 3):
            return 3
        return -1

    """
    " Returns the moving state, the possibilities are listed at the attribute declaration at the top of this file
    """
    def GetMovingState(self):
        return self._movingState

class ImmobileEntity(Entity):
    def StartMovement(self):
        pass
    def IsMoving(self):
        return False
    def Move(self):
        pass

class InventoryItem(Entity):
    # kind is also a name, and value is in cents
    # specify minvalue and maxvalue to randomly decide the value of the item every time "randomize" is called
    # kinds include "money", "roofies", "health", "state", and "buff"
    # target can be "fiendly", "enemy", or "money"
    # healingValue is a percent of the maximum health to heal
    # buffAttr is number multiplied by the current stat (eg [[0,1.2],[1,0.5]])
    # desc is an override of the default item description
    def __init__(self, kind, value, target="friendly", minvalue=-1, maxvalue=-1, name="", healingValue=0, buffAttrs=None, stateNamesToRemove=None, desc=None):
        self._value = 0
        self._name = kind
        self._kind = kind
        self._value = value
        self._target = target
        self._minvalue = minvalue
        self._maxvalue = maxvalue
        self._healingValue = healingValue
        self._buffAttrs = buffAttrs
        self._stateNamesToRemove = stateNamesToRemove
        self._descriptionOverride = desc
        if (name != ""):
            self._name = name

    @property
    def name(self):
        return self._name

    @property
    def target(self):
        return self._target

    @property
    def description(self):
        if self._descriptionOverride is not None:
            return self._descriptionOverride
        if self._kind == "money":
            if (self._value > 100):
                return str(self._value / 100) + " dollars and " + str(self._value % 100) + " cents"
            else:
                return str(self._value) + " cents"
        if self._kind == "state":
            retval = "Cures a creature of being "
            first = True
            for name in stateNamesToRemove:
                if first:
                    first = False
                else:
                    retval += ", "
                retval += name
            return retval
        if self._kind == "buff" or self._kind == "health":
            retval = ""
            if not self._buffAttrs == None:
                retval = "Buffs "
                first = True
                for buff in self._buffAttrs:
                    if first:
                        first = False
                    else:
                        retval += ", "
                    if buff[0] == 0:
                        retval += "speed"
                    elif buff[0] == 1:
                        retval += "attack"
                    elif buff[0] == 3:
                        retval += "deffense"
                if not self._healingValue == 0:
                    retval += " and heals "+str(int(self._healingValue*100))+"% of health"
            else:
                retval = "Heals "+str(int(self._healingValue*100))+"% health health"
            return retval
        return 'BUG: Unknown item type'
        
    def Randomize(self):
        if (self._minvalue > -1 and self._maxvalue > -1):
            self._value = randint(self._minvalue, self._maxvalue)
            if (self._kind == "money"):
                self._name = self.description
    
    # pass in player if roofies is being used
    def Apply(self, creature, isPlayer, player=None, enemy=None):
        person = "The enemy"
        whose = "his"
        if isPlayer:
            person = "You"
            whose = "your"
        if self._kind in ["health", "buff"]:
            creature._currentStats[2] += self._healingValue*creature._attributes[2]
            creature._currentStats[2] = min(creature._currentStats[2], creature._attributes[2])
            if not self._buffAttrs == None:
                for buffAttr in self._buffAttrs:
                    creature._currentStats[buffAttr[0]] *= buffAttr[1]
        if self._kind == "health":
            return person+" used "+self._name+" to heal "+whose+" creature"
        elif self._kind == "buff":
            return person+" used "+self._name+" to buff "+whose+" creature"
        elif self._kind == "state":
            for stateName in self._stateNamesToRemove:
                return person+" used "+self._name+" to make "+whose+" creature not "+stateName
        elif self._kind == "roofies":
            # TODO do a better job here of determining catch chance
            percentHealth = float(creature.health) / creature.maxHealth
            difficulty = max(1, creature.level - self._value) * (percentHealth + .5)
            
            if (random() < difficulty and not player.IsCreaturesFull()):
                player.AddCreature(creature)
                if not enemy == None:
                    enemy.RemoveCreature(creature)
                return [person+" used a "+self._name+" roofie!", person+" caught a "+creature._name]
            else:
                return [person+" used a "+self._name+" roofie!", "The "+creature._name+" got away. :("]
        elif self._kind == "money":
            return "Kaching!"
        return "I have no idea what you just did with that item thar"

# each generic container should have one of these,
# the firts value of the options should add up to 1 where the first value represent the probability of finding that option
GENERIC_CONTAINER_CONTENTS_NAMES_AND_PROBABILITIES = {
        "trashcan": [[0.1, "trash"], [0.99, "money, tiny"], [0.2, "spiked drink"]],
        "dumpster": [[0.1, "trash"], [0.3, "money, tiny"], [0.99, "spiked drink"]],
    }

    # kinds include "money", "roofies", "health", "state", and "buff"
    # target can be "fiendly", "enemy", or "money"
    # attributes are "speed", "attack", "drunkeness", "deffense", and "leveling rate"
POSSIBLE_INVENTORY_ITEMS = {
        "trash": [None, "trash"],
        "money, tiny": [InventoryItem("money", 0, "money", 2, 6)],
        "money, small": [InventoryItem("money", 0, "money", 5, 11)],
        "money, medium": [InventoryItem("money", 0, "money", 10, 16)],
        "money, large": [InventoryItem("money", 0, "money", 15, 21)],
        "money, huge": [InventoryItem("money", 0, "money", 20, 26)],
        "money, gigantic": [InventoryItem("money", 0, "money", 25, 31)],
        "spiked drink": [InventoryItem("roofies", 5, target="enemy", name="spiked drink", desc='A roofie with a low catch chance')],
        "rohypnol": [InventoryItem("roofies", 35, target="enemy", name="rohypnol", desc='A roofie with a medium catch chance')],
        "chloroform": [InventoryItem("roofies", 75, target="enemy", name="chloroform", desc='A roofie with a high catch chance')],
        "speed": [InventoryItem("buff", 80, target="friendly", name="speed", buffAttrs=[[1,1.5],[3,1.5]], healingValue=0.5)],
        "heroine": [InventoryItem("buff", 30, target="friendly", name="heroine", buffAttrs=[[3,1.3]])],
        "thunderbird": [InventoryItem("health", 20, target="friendly", name="thunderbird", healingValue=0.3)],
        "adrenaline": [InventoryItem("health", 30, target="friendly", name="adrenaline", healingValue=0.4)],
    }

# dumpsters and the such
CONTAINER_INDEX = 0
class Container(ImmobileEntity):
    def __init__(self, spriteName, position, gameBoard, plotEvent="", contents=None, contentsName="", contentsDisplayName=""):
        super(Container, self).__init__(spriteName, position, gameBoard)
        
        # generate the contents
        displayText = ""
        self._content = None
        if not(contents == None):
            self._content = contents
        elif (spriteName in GENERIC_CONTAINER_CONTENTS_NAMES_AND_PROBABILITIES):
            contentsName = self._getContentsNameFromRandom(GENERIC_CONTAINER_CONTENTS_NAMES_AND_PROBABILITIES[spriteName])
            self._content = deepcopy(POSSIBLE_INVENTORY_ITEMS[contentsName][0])
            if (self._content == None):
                contentsDisplayName = POSSIBLE_INVENTORY_ITEMS[contentsName][1]
            else:
                self._content.Randomize()
                contentsDisplayName = self._content._name
            if (self._content == None):
                displayText = "Nothing but " + contentsDisplayName + " in here!"
        if (contentsName != "" and self._content != None and displayText == ""):
            displayText = "You found " + contentsDisplayName + "!"
        if (displayText == ""):
            displayText = "Nothing in here!"
        self._plotEvent = plotEvent
        
        # create the display text
        self.AddToDialogueList(self._plotEvent, displayText, endFunction = lambda player, container: container.FinishSearch(player))
    
    def _getContentsNameFromRandom(self, contentsList):
        probability = random()
        sumOfProbabilities = 0
        for content in contentsList:
            sumOfProbabilities += content[0]
            if (sumOfProbabilities >= probability or content == contentsList[-1]):
                return content[1]
    
    def FinishSearch(self, player):
        if not(self._content == None):
            if self._content._kind == "money" or not player.IsInventoryFull():
                self.RemoveFirstDialogue()
                self.AddToDialogueList(self._plotEvent, "Nothing in here")
                if (self._content._kind == "money"):
                    player._money += self._content._value
                else:
                    player.AddItem(deepcopy(self._content))
                self._content = None

class Human(Entity):
    def __init__(self, spriteName, position, gameBoard, secondsToMove, creatures, inventory):
        super(Human, self).__init__(spriteName, position, gameBoard, secondsToMove)
        self._creatures = []
        self._currentCreatureIndex = 0
        self._maxCreatures = 8
        self._inventory = []
        self._maxInventory = 40
        self._money = 0 # cents

        for c in creatures:
            self.AddCreature(c)

        for i in inventory:
            self.AddToInventory(i)

    @property
    def creatures(self):
        return self._creatures[:]

    @property
    def inventory(self):
        return self._inventory[:]

    def AddCreature(self, creature):
        assert not self.IsCreaturesFull()
        self._creatures.append(creature)

    def AddItem(self, item):
        assert not self.IsInventoryFull()
        self._inventory.append(item)

    def HasLiveCreature(self):
        for c in self._creatures:
            if not c.IsDead():
                return True
        return False

    def IsCreaturesFull(self):
        return len(self._creatures) >= self._maxCreatures

    def IsInventoryFull(self):
        return len(self._inventory) >= self._maxInventory

    def RemoveCreature(self, c):
        self._creatures.remove(c)

    def RemoveItem(self, idx):
        del self._inventory[idx]

    def SwapCreatures(self, idx0, idx1):
        temp = self._creatures[idx0]
        self._creatures[idx0] = self._creatures[idx1]
        self._creatures[idx1] = temp
        
    """
    " Attempts to pay for something with money
    " Returns True and reduces the player's money if the requisite amount of money is available
    " Returns False otherwise
    """
    def PayOut(self, quantity):
        if (self._money >= quantity):
            self._money -= quantity
            return True
        return False

class NPC(Human):
    def __init__(self, entityName, spriteName, path, gameBoard, secondsToMove=.5, creatures = [], inventory = []):
        # TODO: Use entityName
        try:
            path[0][0] # is it a list or a position?
            position = path[0]
            self._path = path
            self._movingTo = 0
        except TypeError:
            position = path
            self._path = None
        super(NPC, self).__init__(spriteName, position, gameBoard, secondsToMove, creatures, inventory)
        self.AddFightInfo()

    @property
    def path(self):
        return self._path[:]

    @path.setter
    def path(self, value):
        self._movingTo = 0
        self._path = value

    def AddFightInfo(self, winText = 'You win.', loseText = 'You lose.', winFunction = lambda : None, loseFunction = lambda : None):
        self.winText = winText
        self.loseText = loseText
        self.winFunction = winFunction
        self.loseFunction = loseFunction

    def FinishFight(self, winFunction=lambda: None, loseFunction=lambda: None):
        self.winFunction = winFunction
        self.loseFunction = loseFunction

    def Move(self):
        if self._path is not None and self._movingState == 'notMoving':
            if (self._position == self._path[self._movingTo]).all():
                self._movingTo = (self._movingTo + 1) % len(self._path)
            d = self._path[self._movingTo] - self._position
            if d[0] < 0:
                direction = 'left'
            elif d[0] > 0:
                direction = 'right'
            elif d[1] > 0:
                direction = 'down'
            else:
                direction = 'up'
            self.StartMovement(direction)
        super(NPC, self).Move()
    
    def GetNextMove(self, currentCreature, playerCreature):
        npcHealth = currentCreature._currentStats[2] / currentCreature._attributes[2]
        playerHealth = playerCreature._currentStats[2] / playerCreature._attributes[2]
        
        switchToCreature = None
        healthItem = -1
        buffItem = -1
        hasHealthAttack = False
        for creature in self._creatures:
            if not creature == currentCreature:
                if (creature._currentStats[2] / creature._attributes[2]) > 0.1:
                    switchToCreature = creature
                    break
        for i in range(len(self._inventory)):
            item = self._inventory[i]
            if (item._kind == "health" and (healthItem < 0 or item._healingValue > self._inventory[healthItem]._healingValue)):
                healthItem = i
            if (item._kind == "buff" and (buffItem < 0 or item._buffAttr[1] > self._inventory[buffItem]._buffAttr[1])):
                buffItem = i
        for attack in currentCreature._attacks:
            if attack._recoil < 0:
                hasHealthAttack = True
        
        if (npcHealth > 0.8):
            # choose a debuff attack, or buf or debuf item
            maxBuff = 0
            if (buffItem > -1):
                maxBuff = self._inventory[buffItem]._buffAttr[1]
            buffAttack = -1
            for i in range(len(currentCreature._attacks)):
                attack = currentCreature._attacks[i]
                testNPCCreature = deepcopy(currentCreature)
                testPlayerCreature = deepcopy(playerCreature)
                attack.Attack(testNPCCreature, testPlayerCreature)
                for j in range(2):
                    NPCBuff = (testNPCCreature._currentStats[j] - testNPCCreature._currentStats[j])/testNPCCreature._attributes[j]
                    PlayerBuff = -(testPlayerCreature._currentStats[j] - playerCreature._currentStats[j])/playerCreature._attributes[j]
                    if (NPCBuff + PlayerBuff > maxBuff):
                        maxBuff = NPCBuff + PlayerBuff
                        buffAttack = i

            if (buffAttack > -1):
                return ["attack", currentCreature.attacks[0]]
            elif (buffItem > -1):
                return ["item", buffItem]
        if (npcHealth > 0.1 and npcHealth < 0.3 and (healthItem > -1 or hasHealthAttack)):
            # choose a drunkeness buff item or attack to use and return its index
            mostHealing = 0
            if healthItem > -1:
                mostHealing = self._inventory[healthItem]._healingValue
            bestAttack = -1
            for i in range(currentCreature._attacks):
                attack = currentCreature._attacks[i]
                testNPCCreature = deepcopy(currentCreature)
                testPlayerCreature = deepcopy(playerCreature)
                attack.Attack(testNPCCreature, testPlayerCreature)
                healing = (testNPCCreature._currentStats[2] - testNPCCreature._currentStats[2])/testNPCCreature._attributes[2]
                if (healing > mostHealing):
                    mostHealing = healing
                    bestAttack = i

            if (bestAttack > -1):
                return ["attack", currentCreature.attacks[bestAttack]]
            elif (healthItem > -1):
                return ["item", healthItem]
        if (npcHealth > 0.1 or switchToCreature == None):
            # choose an attack that will do the most damage
            mostDamage = 0
            bestAttack = 0
            for i in range(len(currentCreature._attacks)):
                attack = currentCreature._attacks[i]
                testNPCCreature = deepcopy(currentCreature)
                testPlayerCreature = deepcopy(playerCreature)
                attack.Attack(testNPCCreature, testPlayerCreature)
                damage = -(testPlayerCreature._currentStats[2] - playerCreature._currentStats[2])/playerCreature._attributes[2]
                if (damage > mostDamage):
                    mostDamage = damage
                    bestAttack = i
            return ["attack", currentCreature.attacks[bestAttack]]
        else:
            # switch creatures
            return ["switch", switchToCreature]

class Player(Human):
    def __init__(self, spriteName, position, gameBoard, secondsToMove=.4, creatures = [], inventory = []):
        super(Player, self).__init__(spriteName, position, gameBoard, secondsToMove, creatures, inventory)

        #dictionary of plot events and whether they have been finished/accomplished
        self.plotEvents = {}

    #add a named plot event to the player
    def AddPlotEvent(self, name, done = False):
        self.plotEvents[name] = done;

    #make the player 'accomplish' a plot event
    def FinishPlotEvent(self, name):
        self.plotEvents[name] = True;

if (__name__ == "__main__"):
    # for testing the GetNextMove method
    """from board import Board
    b = Board("test")
    n = NPC("hobo",[0,0],b)
    n.AddCreature(Creature("Programmer"))
    n.AddCreature(Creature("Programmer"))
    n._creatures[0]._currentStats[2] = n._creatures[0]._attributes[2]
    print n.GetNextMove(n._creatures[0],Creature("Dog"))
    print n._creatures[0]"""
    
    #for testing the Apply method of items
    c = Creature("Programmer")
    c._currentStats[2] = 1.0
    print c
    print ""
    print POSSIBLE_INVENTORY_ITEMS["speed"][0].Apply(c, False)
    print ""
    print c
    print ""
    print POSSIBLE_INVENTORY_ITEMS["speed"][0].Apply(c, True)
