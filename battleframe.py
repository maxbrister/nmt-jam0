import collections
import creature
import graphics
import menuframe
import stateframe

from collections import OrderedDict
from creature import Creature
from graphics import DisplayTextBox, Sprite
from menuframe import MenuFrame
from stateframe import StateFrame, stack

class BattleFrame(StateFrame):
    def __init__(self, player, npc):
        super(BattleFrame, self).__init__()
        self._player = player
        self._npc = npc

        self._playerIndex = 0
        self._npcIndex = 0
        self._state = 'player_options' # player_options or show_text
        self._CreateMenu()

    def GetInput(self, inputDictionary):
        if self._state == 'show_text':
            if inputDictionary['a']:
                del self._story[0]
                if len(self._story) <= 0:
                    self._state = 'player_options'

    def Update(self):
        if self._state == 'player_options':
            menu = MenuFrame(self._playerOptions, 'What Now?', (20, 450), 16, 16)
            stack.append(menu)

    def Render(self, ctx, size):
        self._DrawCreature(ctx, 10, self._playerCreature)

        c = Creature('Programmer')
        self._DrawCreature(ctx, 420, self._npcCreature)

        if self._state == 'show_text':
            DisplayTextBox(ctx, self._story[0], (0, 400), (800,200), 20, True)

    @property
    def _playerCreature(self):
        return self._player.creatures[self._playerIndex]

    @property
    def _npcCreature(self):
        return self._npc.creatures[self._playerIndex]
    
    def _CreateMenu(self):
        attacks = OrderedDict()
        for attack in self._playerCreature.attacks:
            attacks[attack.name] = lambda : self._DoPlayerAttack(attack)

        self._playerOptions = OrderedDict()
        self._playerOptions['Attack'] = attacks
        self._playerOptions['Use Item'] = lambda : None
        self._playerOptions['Run Like a MOFO'] = lambda : None
        self._playerOptions['Switch Creatures'] = lambda : None

    def _DoPlayerAttack(self, attack):
        self._story = self._playerCreature.Attack(attack, self._npcCreature)
        self._state = 'show_text'
        

    def _DrawCreature(self, ctx, startx, creature):
        ctx.save()

        HEALTH_WIDTH = 350
        HEALTH_HEIGHT = 34

        ctx.translate(startx, 10)

        ctx.set_source_rgb(.5, .5, .5)
        ctx.rectangle(0, 0, HEALTH_WIDTH, HEALTH_HEIGHT)
        ctx.fill()

        ctx.set_source_rgb(1, 0, 0)
        ctx.rectangle(0, 0, (creature.health / creature.maxHealth) * HEALTH_WIDTH, HEALTH_HEIGHT)
        ctx.fill()
        
        topText = '%s: lvl %s' % (creature.name, creature.level)
        DisplayTextBox(ctx, topText, boxSize=(HEALTH_WIDTH, HEALTH_HEIGHT), DRAW_BACKGROUND=False)

        ctx.translate(0, HEALTH_HEIGHT + 10)
        sprite = Sprite('beer')
        sprite.position = (HEALTH_WIDTH - sprite.width) / 2 - sprite.width / 2, 0
        sprite.Render(ctx)

        ctx.restore()


if __name__ == '__main__':
    import board
    import entity
    import main
    from stateframe import FrameUpdate

    board = board.Board('test')
    player = entity.Player('foo', (0,0), board)
    player.AddCreature(Creature('Dog'))

    npc = entity.Player('bar', (1,0), board)
    npc.AddCreature(Creature('Programmer'))

    stack.append(BattleFrame(player, npc))
    win = main.Window('BattleFrame test')
    win.run(FrameUpdate)
