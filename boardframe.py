from board import Board
from entity import Entity
import numpy
from stateframe import StateFrame, stack

class BoardFrame(StateFrame):
    # multiply by screen size to get dead zone size
    DEAD_ZONE_MUL = numpy.array([.25, .25])
    
    def __init__(self, boardName='test'):
        super(BoardFrame, self).__init__('Continuous')
        self._board = Board(boardName)
        self._player = Entity('bar', (0,0), self._board)

        # center of the camera
        self._camera = self._player.drawPosition + self._board.tileSize * .5

    def GetInput(self, inputDict):
        if inputDict['w']:
            self._player.StartMovement('up')
        if inputDict['a']:
            self._player.StartMovement('left')
        if inputDict['s']:
            self._player.StartMovement('down')
        if inputDict['d']:
            self._player.StartMovement('right')

    def Render(self, ctx, size):
        deadZone = BoardFrame.DEAD_ZONE_MUL * size
        pos = self._player.drawPosition + self._board.tileSize * .5
        self._camera[0] = max(pos[0] - deadZone[0], self._camera[0])
        self._camera[1] = max(pos[1] - deadZone[1], self._camera[1])
        
        self._camera[0] = min(pos[0] + deadZone[0], self._camera[0])
        self._camera[1] = min(pos[1] + deadZone[1], self._camera[1])

        trans = self._camera - numpy.array(size, dtype=numpy.double) * .5
        ctx.translate(*-trans)
        self._board.Render(ctx)

    def Update(self):
        self._player.Move()

if __name__ == '__main__':
    import main
    from stateframe import FrameUpdate
    
    # test BoardFrame
    stack.append(BoardFrame())
    win = main.Window('BoardFrame Test')
    win.run(FrameUpdate)
