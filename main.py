#!/usr/bin/python2
import sys
import pygame
import pygame.locals

class Window(object):
    def __init__(self, name = 'Hobo Sim 2013', size=(800,600)):
        pygame.init()
        self._window = pygame.display.set_mode(size)
        pygame.display.set_caption(name)


if __name__ == '__main__':
    win = Window()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit()
