import math
import dialogueframe
from board import Board
from entity import Entity, Player
import gametime
import numpy
import collections
from stateframe import StateFrame, stack
from menuframe import MenuFrame
from dialogueframe import DialogueFrame
from inventoryframe import InventoryFrame

def MakeCreatureMenu(player, onSelect, filterfn = lambda c: True):
    options = collections.OrderedDict()
    fmt = '{0} lvl: {1} health: {2}%'
    for idx, c in enumerate(player.creatures):
        if filterfn(c):
            if c.IsDead():
                name = fmt.format(c.name, c.level, 'DEAD')
            else:
                name = fmt.format(c.name, c.level,
                                  max(1, int(math.floor(100 * float(c.health / c.maxHealth)))))
            options[name] = lambda idx=idx, c=c: onSelect(idx, c)
    return options

def ShowPauseMenu(player):
    gametime.SetPlaying(False)
    options = collections.OrderedDict()
    options['Continue'] = lambda: None
    creatureOptions = None
    if len(player.creatures) == 1:
        creatureOptions = MakeCreatureMenu(player,
                                           lambda idx, c: None)
    elif len(player.creatures) > 1:
        # sort of an abuse of stuff here
        class SwapMenuControl(object):
            def __init__(self, player):
                self._selectedIndex = -1
                self._player = player
                
            def __call__(self, idx, c):
                if self._selectedIndex < 0:
                    self._selectedIndex = idx
                    options = collections.OrderedDict()
                    options['Swap'] = lambda: 'back'
                    options['Back'] = self._resetSwapSelection
                    return options
                else:
                    self._player.SwapCreatures(idx, self._selectedIndex)
                    del stack[-1]
                    del stack[-1]
                    menu = ShowPauseMenu(self._player)
                    menu.DoSelection(1)
                    return True
                    

            def _resetSwapSelection(self):
                self._selectedIndex = -1
                return 'back'

        mcontrol = SwapMenuControl(player)
        creatureOptions = MakeCreatureMenu(player, mcontrol)
        
                                           
    if creatureOptions is not None:
        options['Creatures'] = creatureOptions
    options['Items'] = InventoryFrame(player)
    options['Exit'] = lambda: exit(0)
    return MenuFrame.Show(options)
    
class BoardFrame(StateFrame):
    # multiply by screen size to get dead zone size
    DEAD_ZONE_MUL = numpy.array([.25, .25])
    
    def __init__(self, boardName='test'):
        super(BoardFrame, self).__init__('Continuous')
        self._board = Board(boardName)
        self._player = Player('hobo', (0,0), self._board)
        self._player.AddPlotEvent('foo')
        self._player.AddPlotEvent('talktoblind')
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
            ShowPauseMenu(self._player)
            return

        if inputDict['i']:
            gametime.SetPlaying(False)
            stack.append(InventoryFrame(self._player))

        other = self._colide(self._player)
        if other is not None:
            self._player.StopMovement()
            self._converse(other)

    def Render(self, ctx, size):
        ctx.save()

        # blow up the pixel art
        size = size[0]/2, size[1]/2
        ctx.scale(2, 2)

        
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
                if entity != self._player and entity._hasDialogue:
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
