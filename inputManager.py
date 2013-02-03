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

#dictionary of keys to look up by char
#doesn't matter if keys are defined or not
#because they automatically get added to the KeysDown
#when they're pressed

keysDownState = {chr(key): False for key in xrange(255)}
keysDown = {chr(key): False for key in xrange(255)}

previousMode = None

def UpdateInputEvent(inputMode='Discrete'):

    global previousMode
    if previousMode != inputMode:
        for k in keysDown:
            keysDown[k] = False
            keysDownState[k] = False
        previousMode = inputMode
    
    eventList = pygame.event.get()

    for evt in eventList:
        if evt.type == QUIT:
            sys.exit(0)

    if inputMode == "Continuous":
        for event in eventList:
            if event.type == KEYDOWN and event.key < 256:
                keysDown[chr(event.key)] = True
            if event.type == KEYUP and event.key < 256:
                keysDown[chr(event.key)] = False
                
    if inputMode == "Discrete":
        #reset all preexisting keypresses
        for key in keysDown:
            keysDown[key] = False

        #find out which keys have been pressed and released
        for event in eventList:
            if event.type == KEYDOWN and event.key < 256:
                keysDownState[chr(event.key)] = True
            if event.type == KEYUP and event.key < 256 and keysDownState[chr(event.key)]:
                keysDownState[chr(event.key)] = False
                keysDown[chr(event.key)] = True
    return keysDown
