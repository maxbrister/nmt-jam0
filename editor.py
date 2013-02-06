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

def TLBR(p0, p1):
    '''
    Given two points of a axis aligned rectangle, determine the top left and bottom right.
    return - tl, br
    '''
    return (array((min(p0[0], p1[0]), min(p0[1], p1[1]))),
            array((max(p0[0], p1[0]), max(p0[1], p1[1]))))

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
        self.selection = None

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
        if btn == 1:
            # click and drag to modify the selection
            # selection[0] -> starting point
            # selection[1] -> ending point
            # selection[3] -> Is mouse in bounds?
            boardPos = self._MouseToBoard(pos)
            if self.board.InRange(boardPos):
                if down:
                    self.selection = [boardPos, boardPos, True]
                else:
                    self._ApplySelection()
            else:
                # only apply selection if iniside board
                if down:
                    self.selection[2] = False
                else:
                    self.selection = None
        elif btn == 3:
            self.panning = down

    def InjectMouseMotion(self, pos, rel):
        if self.panning:
            self.camera -= array(rel)
        elif self.selection is not None:
            boardPos = self._MouseToBoard(pos)
            if self.board.InRange(boardPos):
                self.selection[1] = boardPos
                self.selection[2] = True
            else:
                self.selection[2] = False

    def Render(self, ctx, size):
        ctx.save()
        ctx.translate(*-self.camera)
        self.board.Render(ctx)
        ctx.set_source_rgb(1, 0, 0)
        ctx.set_line_width(.5)
        self.board.RenderLines(ctx)
        if self.selection and self.selection[2]:
            ctx.set_source_rgba(0, 0, 1, .5)
            tl, br = TLBR(*self.selection[:2])
            br += 1
            tl *= self.board.tileSize
            br *= self.board.tileSize
            hw = br - tl
            ctx.rectangle(tl[0], tl[1], hw[0], hw[1])
            ctx.fill()
        ctx.restore()

    def _ApplySelection(self):
        applyList = list()
        revertList = list()
        tl, br = TLBR(*self.selection[:2])
        for x in xrange(tl[0], br[0]+1):
            for y in xrange(tl[1], br[1]+1):
                applyList.append(((x, y), self.tileName))
                revertList.append(((x, y), self.board.GetTileName((x, y))))
        self.redoStack = [(
                lambda: self._ReplaceAllTile(revertList),
                lambda: self._ReplaceAllTile(applyList),
                )]
        self._Redo()
        self.selection = None

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

    def _ReplaceAllTile(self, tileList):
        for pos, tileName in tileList:
            self.board.ReplaceTile(pos, tileName)

    def _SetTile(self, tileName):
        self.tileName = tileName

    def _ShowTileMenu(self):
        tiles = maps.tileset.tiles
        options = {tile: (lambda tile=tile: self._SetTile(tile)) for tile in tiles}
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
    
    
