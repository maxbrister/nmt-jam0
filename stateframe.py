import cairo
import math

from board import Board
from entity import Entity
from inputManager import UpdateInputEvent
import numpy
from pygame.locals import *

stack = [] 

def InitGame():
    main_menu_list = {'Start Game':(lambda : BoardFrame(stack)), 'Exit': (lambda : exit(0))}
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
        self.options = options        #{'title':function/submenu list}
        self.selected = 0
        self.title = 'TEST TITLE YO!'

    def Render(self, ctx, size):
        #ctx.translate (0.1, 0.1) # Changing the current transformation matrix
        ctx.move_to (15, 15)
        ctx.text_path('THIS IS SOME TEXT, YO!')
        #ctx.show_text('This is some text, yo!')
        ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
        ctx.stroke ()




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
    # multiply by screen size to get dead zone size
    DEAD_ZONE_MUL = numpy.array([.25, .25])
    
    def __init__(self, boardName='test'):
        super(BoardFrame, self).__init__()
        self._board = Board(boardName)
        self._player = Entity('foo', (0,0), self._board)

        # center of the camera
        self._camera = self._player.drawPosition + self._board.tileSize * .5

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
        deadZone = BoardFrame.DEAD_ZONE_MUL * size
        pos = self._player.drawPosition + self._board.tileSize * .5
        self._camera[0] = max(pos[0] - deadZone[0], self._camera[0])
        self._camera[1] = max(pos[1] - deadZone[1], self._camera[1])
        
        self._camera[0] = min(pos[0] + deadZone[0], self._camera[0])
        self._camera[1] = min(pos[1] + deadZone[1], self._camera[1])

        trans = numpy.array(self._camera - numpy.array(size, dtype=numpy.double) * .5, dtype=numpy.int)
        ctx.translate(*-trans)
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
    
    # test BoardFrame
    stack.append(BoardFrame())
    win = main.Window('BoardFrame Test')
    win.run(FrameUpdate)
