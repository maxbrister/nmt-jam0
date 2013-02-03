import collections
import gametime
import graphics
import numpy

from gametime import GameTime
from graphics import Sprite
from creature import Creature
from copy import deepcopy
from random import random, randint

"""
" The entity class should be used for anything that has a sprite, position, and can interact with other entities.
" Entities have the movement methods StartMovement, IsMoving, and Move. For immobile entities (such as a flower pot), use the ImmobileEntity class.
" The interact method is an abstract method, meant to be implemented more in later classes.
"""

class Entity(object):
    DIRECTION_TO_ANIM = ['up', 'right', 'down', 'left', '']
    DIRECTION_TO_DELTA = numpy.array([(0,-1), (1,0), (0,1), (-1,0)])
    
    """
    " @spriteName the graphical representation of the Entity
    " @Position a numpy.array
    " @gameBoard the gameboard object
    " @secondsToMove the number of seconds it should take to finish the animated movement
    """
    def __init__(self, spriteName, position, gameBoard, secondsToMove=0.1):
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

    """
    " Used by the game loop to determine if the entity is moving or not
    """
    def IsMoving(self):
        if (self._movingState == "notMoving" or self._movingState == "finishing"):
            return False
        return True

    def Render(self, ctx):
        self._sprite.SetFrame(Entity.DIRECTION_TO_ANIM[self._movingDirection], self._movingFrame)
        self._sprite.Render(ctx)

    """
    " Stops the movement of the entity and resets its movement data
    """
    def StopMovement(self, finishMovement = False):
        if (finishMovement):
            self._Move()
        self._movingState = "notMoving"
        self._movingFrame = 0
        self._movingDirection = 4 # stoped

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
    def __init__(self, kind, value, minvalue=-1, maxvalue=-1):
        self._value = 0
        self._name = kind
        self._kind = kind
        self._value = value
        self._minvalue = minvalue
        self._maxvalue = maxvalue
        
    def Randomize(self):
        if (self._minvalue > -1 and self._maxvalue > -1):
            self._value = randint(self._minvalue, self._maxvalue)
            if (self._kind == "money"):
                if (self._value > 100):
                    self._name = str(self._value / 100) + " dollars and " + str(self._value % 100) + " cents"
                else:
                    self._name = str(self._value) + " cents"

# each generic container should have one of these,
# the firts value of the options should add up to 1 where the first value represent the probability of finding that option
GENERIC_CONTAINER_CONTENTS_NAMES_AND_PROBABILITIES = {
        "trashcan": [[0.5, "trash"], [0.3, "money, tiny"], [0.2, "mouse trap"]]
    }

GENERIC_CONTAINER_CONTENTS = {
        "trash": [None, "trash"],
        "money, tiny": [InventoryItem("money", 0, 1, 6)],
        "mouse trap": [InventoryItem("mouse trap", 5)]
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
            self._content = deepcopy(GENERIC_CONTAINER_CONTENTS[contentsName][0])
            if (self._content == None):
                contentsDisplayName = GENERIC_CONTAINER_CONTENTS[contentsName][1]
            else:
                self._content.Randomize()
                contentsDisplayName = self._content._name
            if (self._content == None):
                displayText = "Nothing but " + contentsDisplayName + " in here"
        if (contentsName != "" and self._content != None and displayText == ""):
            displayText = "You found " + contentsDisplayName
        if (displayText == ""):
            displayText = "Nothing in here"
        self._plotEvent = plotEvent
        print contentsName, contentsDisplayName, self._content, displayText, self._plotEvent
        
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
            if not player.IsInventoryFull():
                self.RemoveFirstDialogue()
                self.AddToDialogueList(self._plotEvent, "Nothing in here")
                player.AddItem(deepcopy(self._content))
                self._content = None

# ABC for NPC and Player
class Human(Entity):
    def __init__(self, spriteName, position, gameBoard, secondsToMove, creatures, inventory):
        super(Human, self).__init__(spriteName, position, gameBoard, secondsToMove)
        self._creatures = []
        self._currentCreatureIndex = 0
        self._maxCreatures = 8
        self._inventory = []
        self._maxInventory = 40

        for c in creatures:
            self.AddCreature(c)

        for i in inventory:
            self.AddToInventory(i)

    @property
    def creatures(self):
        return self._creatures[:]

    def AddCreature(self, creature):
        assert not self.IsCreaturesFull()
        self._creatures.append(creature)

    def AddItem(self, item):
        assert not self.IsInventoryFull()
        self._inventory.append(item)

    def IsCreaturesFull(self):
        return len(self._creatures) >= self._maxCreatures

    def IsInventoryFull(self):
        return len(self._inventory) >= self._maxInventory

    def RemoveCreature(self, idx):
        del self._creatures[idx]

    def RemoveItem(self, idx):
        del self._inventory[idx]

class NPC(Human):
    def __init__(self, spriteName, path, gameBoard, secondsToMove=.5, creatures = [], inventory = []):
        try:
            path[0][0] # is it a list or a position?
            position = path[0]
            self._path = path
            self._movingTo = 0
        except TypeError:
            position = path
            self._path = None
        super(NPC, self).__init__(spriteName, position, gameBoard, secondsToMove, creatures, inventory)

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

class Player(Human):
    def __init__(self, spriteName, position, gameBoard, secondsToMove=.1, creatures = [], inventory = []):
        super(Player, self).__init__(spriteName, position, gameBoard, secondsToMove, creatures, inventory)

        #dictionary of plot events and whether they have been finished/accomplished
        self.plotEvents = {}

    #add a named plot event to the player
    def AddPlotEvent(self, name, done = False):
        self.plotEvents[name] = True;

    #make the player 'accomplish' a plot event
    def FinishPlotEvent(self, name):
        self.plotEvents[name] = True;

if (__name__ == "__main__"):
    class Entity_GameBoardTest:
        def __init__(self):
            pass
        def Movable(self, pos):
            x, y = pos
            return set()
            return set([(x,y), (x-1,y), (x+1,y), (x,y-1), (x,y+1)])
        def Move(self, entity, oldPosition, newPosition):
            pass

    import time
    g = Entity_GameBoardTest()
    e = Entity("spritestuff", (0, 0), g)
    while (True):
        if not (e.IsMoving()):
            e.StartMovement("right")
        print e.Move()
        print e.GetMovingState()
        time.sleep(0.10)
