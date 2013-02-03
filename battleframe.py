import creature
import graphics
import menuframe
import stateframe

from creature import Creature
from graphics import DisplayTextBox, Sprite
from menuframe import MenuFrame
from stateframe import StateFrame, stack

class BattleFrame(StateFrame):
    def __init__(self, player, npc):
        super(BattleFrame, self).__init__()
        self._player = player
        self._npc = npc

        self._playerOptions = {'Attack' : (lambda : None),
                               'Use Item' : (lambda : None),
                               'Run' : (lambda : None),
                               'Switch' : (lambda : None)}
        self._state = 'player_options'

    def ProcessInput(self, inputDictionary):
        pass

    def Update(self):
        if self._state == 'player_options':
            menu = MenuFrame(self._playerOptions, position=(20, 450), fontSize=16)
            stack.append(menu)

    def Render(self, ctx, size):
        c = Creature('Dog')
        self._DrawCreature(ctx, 10, c)

        c = Creature('Programmer')
        self._DrawCreature(ctx, 420, c)

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
    import main
    from stateframe import FrameUpdate, stack

    stack.append(BattleFrame(None, None))
    win = main.Window('BattleFrame test')
    win.run(FrameUpdate)
