import dialogueframe
from board import Board
from entity import Entity, Player
import gametime
import numpy
from stateframe import StateFrame, stack
from menuframe import MenuFrame
from dialogueframe import DialogueFrame

pause_menu = main_menu_list = {'Continue': (lambda: None), 'Submenu': {'Back': (lambda: None)}, 'Exit': (lambda : exit(0))}

class BoardFrame(StateFrame):
    # multiply by screen size to get dead zone size
    DEAD_ZONE_MUL = numpy.array([.25, .25])
    
    def __init__(self, boardName='test'):
        super(BoardFrame, self).__init__('Continuous')
        self._board = Board(boardName)
        self._player = Player('hobofront', (0,0), self._board)
        self._player.AddPlotEvent('foo')
        self._player.AddPlotEvent('bar')
        self._player.FinishPlotEvent('foo')

        # center of the camera
        self._camera = self._player.drawPosition + self._board.tileSize * .5
        self._converseInPosition = None

    def GetInput(self, inputDict):
        if inputDict['w']:
            self._player.StartMovement('up')
        if inputDict['a']:
            self._player.StartMovement('left')
        if inputDict['s']:
            self._player.StartMovement('down')
        if inputDict['d']:
            self._player.StartMovement('right')
        if inputDict['p'] or inputDict[chr(27)]:
            gametime.SetPlaying(False)
            stack.append(MenuFrame(pause_menu, 'Pause'))

        other = self._colide(self._player)
        if other is not None:
            self._player.StopMovement()
            self._converse(other)

    def Render(self, ctx, size):
        ctx.save()
        deadZone = BoardFrame.DEAD_ZONE_MUL * size
        pos = self._player.drawPosition + self._board.tileSize * .5
        self._camera[0] = max(pos[0] - deadZone[0], self._camera[0])
        self._camera[1] = max(pos[1] - deadZone[1], self._camera[1])
        
        self._camera[0] = min(pos[0] + deadZone[0], self._camera[0])
        self._camera[1] = min(pos[1] + deadZone[1], self._camera[1])

        trans = self._camera - numpy.array(size, dtype=numpy.double) * .5
        ctx.translate(*-trans)
        self._board.Render(ctx)
        ctx.restore()

    def Update(self):
        gametime.SetPlaying(True)
        gametime.Update()
        for entity in self._board.entities:
            entity.Move()

        if tuple(self._player.position) != self._converseInPosition:
            self._converseInPosition = None
            for entity in self._board.entities:
                if entity != self._player:
                    target = self._colide(entity)
                    if target == self._player:
                        self._converseInPosition = tuple(self._player.position)
                        stack.append(DialogueFrame(self._player, entity))

    def _colide(self, ent):
        tpos = ent.targetPosition
        if self._board.InRange(tpos):
            target = self._board.GetEntity(tpos)
            if target is not None and target != ent:
                return target
        return None

    def _converse(self, other):
        gametime.SetPlaying(False)
        stack.append(DialogueFrame(self._player, other))

if __name__ == '__main__':
    import main
    from stateframe import FrameUpdate
    
    # test BoardFrame
    stack.append(BoardFrame())
    win = main.Window('BoardFrame Test')
    win.run(FrameUpdate)
