from board import Board
from entity import Entity
from inputManager import UpdateInputEvent
import numpy
from pygame.locals import *

from menuframe import MainMenuFrame

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


if __name__ == '__main__':
    import main
    
    # test BoardFrame
    stack.append(BoardFrame())
    win = main.Window('BoardFrame Test')
    win.run(FrameUpdate)
