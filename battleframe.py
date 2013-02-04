import collections
import creature
import graphics
import math
import menuframe
import stateframe

from collections import OrderedDict
from creature import Creature
from graphics import DisplayTextBox, Sprite
from menuframe import MenuFrame
from stateframe import StateFrame

class BattleFrame(StateFrame):
    def __init__(self, player, npc):
        super(BattleFrame, self).__init__()
        self._player = player
        self._npc = npc

        self._turn = 1 # 0 for player, 1 for enemy
        self._playerIndex = 0
        self._npcIndex = 0
        # player-options | battle-results | turn-start | lose | win | select-creature
        self._state = 'battle-results' # announce whos turn it is next
        self._NextTurn()

    def GetInput(self, inputDictionary):
        if inputDictionary['a']:
            if self._state in ['battle-results', 'turn-start']:
                del self._story[0]
                if len(self._story) <= 0:
                    self._NextTurn()
            elif self._state == 'win':
                # TODO advance the player's state
                self.KillSelf()
            elif self._state == 'lose':
                self.KillSelf()
                if len(stateframe.stack) > 0:
                    stateframe.stack = [stateframe.stack[0]] # back to main menu

    def Update(self):
        if self._state == 'player-options':
            menu = MenuFrame(self._CreateMenu(), 'What Now?', (20, 400), 16, 16)
            stateframe.stack.append(menu)
        elif self._state == 'select-creature':
            menu = MenuFrame(self._CreateSwitchMenu(), 'Next Victim', (20, 400), 16, 16)
            stateframe.stack.append(menu)

    def Render(self, ctx, size):
        self._DrawCreature(ctx, 10, self._playerCreature)
        self._DrawCreature(ctx, 420, self._npcCreature)

        text = None
        if self._state in ['battle-results', 'turn-start']:
            text = self._story[0]
        elif self._state == 'lose':
            text = 'You lose :\'('
        elif self._state == 'win':
            textg = 'OMG OMG YOU WIN!!11!!11!!!'

        if text is not None:
            DisplayTextBox(ctx, text, (0, 400), (800,200), 20, True)

    @property
    def _playerCreature(self):
        return self._player.creatures[self._playerIndex]

    @property
    def _npcCreature(self):
        return self._npc.creatures[self._npcIndex]


    def _CreateSwitchMenu(self, hasBack = False):
        ret = OrderedDict()
        if hasBack:
            ret['Back'] = lambda : None
        for idx, c in enumerate(self._player.creatures):
            if not c.IsDead() and idx != self._playerIndex:
                name = '{0} lvl: {1} health: {2}%'.format(
                    c.name,
                    c.level,
                    max(1, int(math.floor(100 * float(c.health / c.maxHealth))))
                    )

                def DoSwitch():
                    self._playerIndex = idx
                    self._story = ['Go {0}!!!'.format(c.name)]
                    self._state = 'battle-results'
                ret[name] = DoSwitch
        return ret
    
    def _CreateMenu(self):
        def DoPlayerAttack(attack):
            self._story = self._playerCreature.Attack(attack, self._npcCreature, True)
            self._state = 'battle-results'
            
        attacks = OrderedDict()
        for attack in self._playerCreature.attacks:
            attacks[attack.name] = lambda attack=attack : DoPlayerAttack(attack)

        def TryRun():
            self._story = ['You think about running, but decide that you are too lazy.']
            self._state = 'battle-results'

        def DoNothing():
            self._story = ['You quack some and try to fly.']
            self._state = 'battle-results'

        playerOptions = OrderedDict()
        playerOptions['Attack'] = attacks
        playerOptions['Use Item'] = lambda : None
        playerOptions['Switch Creatures'] = self._CreateSwitchMenu(True)
        playerOptions['Run Like a MOFO'] = TryRun
        playerOptions['Sit Like a Duck'] = DoNothing
        return playerOptions

    def _DoNPCMove(self):
        move = self._npc.GetNextMove(self._npcCreature, self._playerCreature)
        self._story = list()
        if move[0] == 'attack':
            attack = move[1]
            self._story += self._npcCreature.Attack(attack, self._playerCreature)
        elif move[0] == 'item':
            self._story.append('Items do not work.')
        elif move[0] == 'switch':
            self._story.append('The enemy switches creatures.')
            self._npcIndex = move[1]
        else:
            self._story.append('The game is FULL of bugs. The NPC does nothing in protest.')

        self._state = 'battle-results'

    def _DrawCreature(self, ctx, startx, creature):
        ctx.save()

        HEALTH_WIDTH = 350
        HEALTH_HEIGHT = 34

        ctx.translate(startx, 10)

        ctx.set_source_rgb(.5, .5, .5)
        ctx.rectangle(0, 0, HEALTH_WIDTH, HEALTH_HEIGHT)
        ctx.fill()

        if not creature.IsDead():
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

    def _NextTurn(self):
        if not self._player.HasLiveCreature():
            self._state = 'lose'
            return

        if not self._npc.HasLiveCreature():
            self._state = 'win'
            return

        if self._playerCreature.IsDead():
            # The player must switch creatures
            self._state = 'select-creature'
            return

        if self._npcCreature.IsDead():
            for idx, c in enumerate(self._npc.creatures):
                if not c.IsDead():
                    self._npcIndex = idx
                    self._story = ['The enemy uses {0}!!!'.format(c.name)]
                    self._state = 'battle-results'
                    break
            return

        if self._state != 'turn-start':
            # increment the turn
            self._turn = (self._turn + 1) % 2
            self._state = 'turn-start'
            if self._turn == 0:
                self._story = ['Your turn, you should do something or not.']
            else:
                self._story = ['The enemies turn, OH NOES.']
            return

        if self._turn == 0:
            self._state = 'player-options'
        else:
            self._DoNPCMove()


if __name__ == '__main__':
    import board
    import entity
    import main
    from stateframe import FrameUpdate

    board = board.Board('test')
    player = entity.Player('foo', (0,0), board)
    player.AddCreature(Creature('Programmer'))
    player.AddCreature(Creature('Dog'))

    npc = entity.NPC('bar', (1,0), board)
    npc.AddCreature(Creature('Dog'))
    npc.AddCreature(Creature('Programmer'))

    stateframe.stack.append(BattleFrame(player, npc))
    win = main.Window('BattleFrame test')
    win.run(FrameUpdate)
