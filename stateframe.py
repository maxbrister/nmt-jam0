from board import Board
from entity import Entity
from inputManager import UpdateInputEvent
import numpy
from pygame.locals import *

stack = [] 

def FrameUpdate(ctx,size):
    stack[-1].GetInput(UpdateInputEvent(stack[-1].inputMode))
    if len(stack) == 0:
        return False
    stack[-1].Update()
    if len(stack) == 0:
        return False
    stack[-1].Render(ctx, size)
    return len(stack) > 0


class StateFrame(object):
    def __init__(self, inputMode='Discrete'):
        self.inputMode = inputMode

    def GetInput(self, inputDic):
        # subclass should override
        pass

    def Update(self):
        # subclass should override
        pass

    def Render(self, ctx, size):
        # subclass should override
        pass

    def RenderParent(self, ctx, size):
        i = stack.index(self)
        if i > 0 :
            stack[i-1].Render(ctx, size)

    def Show(self):
        assert self not in stack
        stack.append(self)

    def KillSelf(self):
        stack.pop()
