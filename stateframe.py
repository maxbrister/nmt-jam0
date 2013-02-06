from board import Board
from entity import Entity
from inputManager import UpdateInputEvent
import numpy
from pygame.locals import *

stack = [] 

def FrameUpdate(ctx,size):
    if stack[-1].keyToEvent:
        UpdateInputEvent(stack[-1], stack[-1].keyToEvent)
    else:
        UpdateInputEvent(stack[-1])
    if len(stack) == 0:
        return False
    
    stack[-1].Update()
    if len(stack) == 0:
        return False
    
    stack[-1].Render(ctx, size)
    return len(stack) > 0


class StateFrame(object):
    def __init__(self, keyToEvent=None):
        self.keyToEvent = keyToEvent

    @property
    def visible(self):
        return self in stack

    def MaybeInjectInput(self, event, down):
        if self._TopFrame():
            self.InjectInput(event, down)

    def MaybeInjectMouseMotion(self, pos, rel):
        if self._TopFrame():
            self.InjectMouseMotion(pos, rel)

    def MaybeInjectMouseButton(self, btn, pos, down):
        if self._TopFrame():
            self.InjectMouseButton(btn, pos, down)

    def InjectInput(self, event, down):
        # subclass should override
        pass

    def InjectMouseButton(self, btn, pos, down):
        # subclass should override
        pass

    def InjectMouseMotion(self, pos, rel):
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
        assert not self.visible
        stack.append(self)

    def KillSelf(self):
        del stack[stack.index(self)]

    def Quit(self):
        del stack[:]

    def _TopFrame(self):
        return len(stack) > 0 and stack[-1] == self
