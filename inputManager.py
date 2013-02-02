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
keysDown = {'w': False,
            'a': False,
            's': False,
            'd': False,
            'q': False,
            'e': False
           }

def getInputEvent():
    
    eventList = pygame.event.get()
    for event in eventList:
        if event.type == KEYDOWN and event.key < 256:
            keysDown[chr(event.key)] = True;
        if event.type == KEYUP and event.key < 256:
            keysDown[chr(event.key)] = False;
    
        
        
