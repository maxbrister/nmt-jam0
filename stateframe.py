from board import Board
from entity import Entity
from inputManager import UpdateInputEvent, SetContinuousInputMode
import numpy
from pygame.locals import *

stack = [] 

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
