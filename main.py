#!/usr/bin/python2
import sys
import pygame
import pygame.locals
import cairo
import numpy
import math
import Image

import graphics

from gamestate import FrameUpdate, InitGame

class Window(object):
    def __init__(self, name = 'Hobo Sim 2013', size=(800,600)):
        # initialize pygame
        pygame.init()
        self._size = size
        self._window = pygame.display.set_mode(size)
        pygame.display.set_caption(name)

        # data to talk between pygame and cairo
        self._data = numpy.empty(size[0] * size[1] * 4, dtype=numpy.int8)

        # initialize cairo
        self._surface = cairo.ImageSurface.create_for_data(self._data, cairo.FORMAT_ARGB32, size[0], size[1], size[0] * 4)
        

    def run(self, callback):
        # test rendering

        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    sys.exit()

            ctx = cairo.Context(self._surface)
            if not callback(ctx, self._size):
                return
            img = Image.frombuffer('RGBA', (self._surface.get_width(),
                                            self._surface.get_height()),
                                   self._surface.get_data(), 'raw', 'BGRA', 0, 1)
            img = img.tostring('raw', 'RGBA', 0, 1)
            psurf = pygame.image.frombuffer(img, self._size, 'RGBA')
            self._window.blit(psurf, (0, 0))
            pygame.display.flip()

if __name__ == '__main__':
    sprite = graphics.Sprite('test')
    win = Window()
    InitGame()        #Places the main menu in the stack
    win.run(FrameUpdate)
    
