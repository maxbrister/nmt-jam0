import sys
import pygame
from  pygame.locals import *
import cairo
import numpy
import math
import Image

"""
run getInputEvent and look at keysDown (indexed by key char)
to see which keys are down.
"""

pygame.init()
InputMode = "Discrete"

#dictionary of keys to look up by char
#doesn't matter if keys are defined or not
#because they automatically get added to the KeysDown
#when they're pressed

keysDown = dict([(chr(key), False) for key in xrange(255)])

def UpdateInputEvent():
    
    eventList = pygame.event.get()

    if InputMode == "Continuous":
        for event in eventList:
            if event.type == KEYDOWN and event.key < 256:
                keysDown[chr(event.key)] = True
            if event.type == KEYUP and event.key < 256:
                keysDown[chr(event.key)] = False
                
    if InputMode == "Discrete":
        #reset all preexisting keypresses
        for key in keysDown:
            keysDown[key] = False

        #find out which keys have been pressed and released
        for event in eventList:
            if event.type == KEYUP and event.key < 256:
                keysDown[chr(event.key)] = True
    return keysDown


#makes keysDown register all keys currently down
def SetContinuousInputMode():
    InputMode = "Continuous"


#makes keysDown register all keys pressed and released
def SetDiscreteInputMode():
    InputMode = "Discrete"
