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
eventsDown = {}
heldOverRelease = set()

previousMode = None

def IncEvent(evt):
    if evt in eventsDown:
        eventsDown[evt] += 1
    else:
        eventsDown[evt] = 1

def DecEvent(evt):
    if evt in eventsDown:
        val = eventsDown[evt]
        val -= 1
        if val <= 0:
            del eventsDown[evt]
        else:
            eventsDown[evt] = val
        return val
    return -1

def UpdateInputEvent(inputMode, dest, keyToEvent={
        K_w: 'up',
        K_a: 'left',
        K_s: 'down',
        K_d: 'right',
        K_i: 'inventory',
        K_p: 'pause',
        K_ESCAPE: 'pause',
        K_RETURN: 'enter'
        }):

    global previousMode
    global heldOverRelease
    assert inputMode in ['Continuous', 'Discrete']
    isContinous = inputMode == 'Continuous'
    if previousMode != inputMode:
        eventsDown.clear()
        previousMode = inputMode
        heldOverRelease.clear()
    
    eventList = pygame.event.get()

    newInject = set()
    previousHeldOver = heldOverRelease
    heldOverRelease = set()
    for event in eventList:
        if event.type == KEYDOWN and event.key in keyToEvent:
            evt = keyToEvent[event.key]
            IncEvent(evt)
            dest.InjectInput(evt, True)
            newInject.add(evt)
            if evt in previousHeldOver:
                previousHeldOver.remove(evt)
                
        if event.type == KEYUP and event.key in keyToEvent:
            evt = keyToEvent[event.key]
            if DecEvent(evt) == 0:
                if not isContinous or evt not in newInject:
                    dest.InjectInput(evt, False)
                else:
                    heldOverRelease.add(evt)
                
        if event.type == QUIT:
            dest.Quit()

    for evt in previousHeldOver:
        dest.InjectInput(evt, False)

            
    for evt in eventsDown.keys():
        dest.InjectInput(evt, True)
