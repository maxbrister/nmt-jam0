from board import Board
from entity import Entity
from inputManager import UpdateInputEvent
from pygame.locals import *

stack = [] 
main_menu_list = ['Start Game', lambda : BoardFrame(stack), 'Exit', lambda : exit(0)]


def InitGame():
    mainMenu = MainMenuFrame(main_menu_list)
    stack.append(mainMenu)

def FrameUpdate(ctx,size):
    stack[-1].GetInput(UpdateInputEvent())
    if len(stack) == 0:
        return False
    stack[-1].Update()
    if len(stack) == 0:
        return False
    stack[-1].Render(ctx, size)
    return len(stack) > 0


class StateFrame(object):
    def __init__(self):
        pass

    def GetInput(self, inputDic):
        # subclass should override
        pass

    def Update(self):
        # subclass should override
        pass

    def Render(self, ctx, size):
        # subclass should override
        pass

    def KillSelf(self):
        stack.pop()


'''
Options = [('name', element)]
where if element is a list, sub-menu
otherwise, it is a function. This function will
always be appended to the stack frame, for convenience.

By the way, we need global game shit... like a player?
And a board?

YEah... things, man...

I forgot to add menu titles. I can take care of that later.
'''
class MainMenuFrame(StateFrame):
    def __init__(self, options):
        super(MainMenuFrame, self).__init__()
        self.options = options
        self.selected = 0

    def Render(self, ctx, size):
        for option in self.options:
            print option[0]

        print '*** %s' % (self.options[self.selected][0])

    def GetInput(self, input_dict):
        if input_dict['w']:
            self.selected = (self.selected - 1) % len(self.options)
        if input_dict['s']:
            self.selected = (self.selected + 1) % len(self.options)
        if input_dict['a']:        #I have no idea how to handle enter...
            if isinstance(self.options[self.selected][1], list):
                stack.append(MainMenuFrame(self.options[self.selected][1]))
            else:
                stack.append(self.options[self.selected][1]())

class BoardFrame(StateFrame):
    def __init__(self, boardName='test'):
        super(BoardFrame, self).__init__()
        self._board = Board(boardName)
        self._player = Entity('foo', (0,0), self._board)

    def GetInput(self, inputDict):
        if inputDict['w']:
            self._player.StartMovement('up')
        if inputDict['a']:
            self._player.StartMovement('left')
        if inputDict['s']:
            self._player.StartMovement('down')
        if inputDict['d']:
            self._player.StartMovement('right')

    def Render(self, ctx, size):
        self._board.Render(ctx)
        self._player.Render(ctx)

    def Update(self):
        self._player.Move()

class BattleFrame(StateFrame):
    def __init__(self, player1, player2):
        # check if player2 is an npc
        pass

    def ProcessInput(self, inputDictionary):
        pass

    def Update(self):
        pass

    def Render(self, ctx, size):
        pass

    def KillSelf(self):
        stack.pop()

class BattleMenuFrame(StateFrame):
    """
    " @battleFrame the menu needs to return to the battle frame the option that the player chooses
    " @player used to determine what options are available
    """
    def __init__(self, battleFrame, player):
        pass

    def ProcessInput(self, inputDictionary):
        pass

    def Update(self):
        pass

    def Render(self, ctx, size):
        pass

    def KillSelf(self):
        stack.pop()

if __name__ == '__main__':
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

    ATTRIBUTE_NAME_TO_VALUE = ["speed", "damage", "drunkeness", "leveling_rate"]
    CREATURES = {
        "Programmer": {"attributes": (2.0, 0.5, 5.0, 1.3),
                       "attacks": ("Passive Agressive Sticky Notes", "Insult Your Code", "Use Star Trek Trivia", "Kick Shins"),
                       "attackLevels": (0, 0, 0, 0) }
        "Dog": {"attributes": (0.7, 2.0, 15.0, 1.1),
                "attacks": ("Bite", "Chew Bones", "Growl Menacingly", "Eat Shoes"),
                "attackLevels": (0, 0, 0, 0) }
        }
    CREATURE_STATES = ["normal", "sleeping"]

    class Creature(object):
        def __init__(self, creatureType):
            # each action is a tuple (action name, damage multiplier)
            self._actionsList = set([("Bite",1.0), ("Bitch Slap",1.5)])
            self._attributes = CREATURES[creatureType]
        def GetStat(self, statName):
            return self._attributes[statName]

    class Player(object):
        def __init__(self):
            self._creatures = (Creature("Programmer"), Creature("Black Woman"))
            self._currentCreature = 0
        def GetCurrentCreature(self):
            return self._currentCreature
        def SetCurrentCreature(self, creatureIndex):
            
    
    # test BoardFrame
    stack.append(BoardFrame())
    win = main.Window('BoardFrame Test')
    win.run(FrameUpdate)
