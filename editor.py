#!/usr/bin/python2
import board
import maps.tileset
import menuframe
import numpy
import pygame.locals
import re
import stateframe

from board import Board
from menuframe import MenuFrame
from numpy import array
from pygame.locals import *

class EditorFrame(stateframe.StateFrame):
    def __init__(self, board):
        super(EditorFrame, self).__init__({
                K_m: 'menu',
                K_s: 'save',
                K_ESCAPE: 'exit',
                K_u: 'undo',
                K_r: 'redo'
                })
        self.board = board
        self.camera = array((0, 0))
        self.panning = False
        self.undoStack = list()
        self.redoStack = list()
        self.tileName = 'blank'

    def InjectInput(self, event, down):
        if down:
            return
        
        if event == 'menu':
            self._ShowTileMenu()
        elif event == 'save':
            self.board.SaveTiles()
        elif event == 'undo':
            self._Undo()
        elif event == 'redo':
            self._Redo()
        elif event == 'exit':
            self.KillSelf()

    def InjectMouseButton(self, btn, pos, down):
        if btn == 1 and not down:
            boardPos = self._MouseToBoard(pos)
            if self.board.InRange(boardPos):
                oldName = self.board.GetTileName(boardPos)
                newName = self.tileName
                self.redoStack.append((
                        lambda: self.board.ReplaceTile(boardPos, oldName),
                        lambda: self.board.ReplaceTile(boardPos, newName)))
                self._Redo()
        elif btn == 3:
            self.panning = down

    def InjectMouseMotion(self, pos, rel):
        if self.panning:
            self.camera -= array(rel)

    def Render(self, ctx, size):
        ctx.save()
        ctx.translate(*-self.camera)
        self.board.Render(ctx)
        ctx.set_source_rgb(1, 0, 0)
        ctx.set_line_width(.5)
        self.board.RenderLines(ctx)
        ctx.restore()

    def _MouseToBoard(self, pos):
        pos = array(pos)
        pos += self.camera
        pos /= board.tileSize
        return array(pos, dtype=numpy.int)

    def _Redo(self):
        if len(self.redoStack) > 0:
            action = self.redoStack[-1]
            del self.redoStack[-1]
            self.undoStack.append(action)
            action[1]()

    def _SetTile(self, tileName):
        self.tileName = tileName

    def _ShowTileMenu(self):
        tiles = maps.tileset.tiles
        options = {tile: self._SetTile(tile) for tile in tiles}
        MenuFrame.Show(options, position=(650, 0), displayItems=23)

    def _Undo(self):
        if len(self.undoStack) > 0:
            action = self.undoStack[-1]
            del self.undoStack[-1]
            self.redoStack.append(action)
            action[0]()

def PrintUsage(cond):
    if cond:
        print 'USAGE: editor.py boardName [resize XXxYY]'
        exit(1)

if __name__ == '__main__':
    import main
    import sys

    resize = False
    PrintUsage(len(sys.argv) not in [2, 4] or (len(sys.argv) > 1 and sys.argv[1] in ['help', '--help', '-help']))
        
    if len(sys.argv) == 4:
        resize = True
        PrintUsage(sys.argv[2].lower() != reisze)
        match = re.match(r'^(?P<width>\d+)[xX](?P<height>\d+)$')
        PrintUsage(not match)
        width = int(match.group('width'))
        height = int(match.group('height'))

    boardName = sys.argv[1]
    board = Board(boardName)
    stateframe.stack.append(EditorFrame(board))

    win = main.Window('{0} Editor'.format(main.GAME_NAME))
    win.run(stateframe.FrameUpdate)
    
    
