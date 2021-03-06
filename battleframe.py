import boardframe
import collections
import creature
import dialogueframe
import graphics
import inventoryframe
import menuframe
import stateframe

from boardframe import MakeCreatureMenu
from collections import OrderedDict
from creature import Creature
from dialogueframe import DialogueFrame
from graphics import DisplayTextBox, Sprite, SpriteError
from inventoryframe import InventoryFrame
from menuframe import MenuFrame
from stateframe import StateFrame

class BattleEndError(Exception):
    pass

class BattleFrame(StateFrame):
    def __init__(self, player, npc, winText, loseText, winFunction, loseFunction):
        super(BattleFrame, self).__init__()
        assert len(player.creatures) > 0
        assert len(npc.creatures) > 0
        self._player = player
        self._npc = npc
        self._winFunction = winFunction
        self._loseFunction = loseFunction

        self._winText = winText
        self._loseText = loseText

        self._playerCreature = self._player.creatures[0]
        self._npcCreature = self._npc.creatures[0]
        self._runner = self._RunGame()


    def Update(self):
        try:
            self._runner.next()
        except StopIteration:
            if self.visible:
                self.KillSelf()

    def Render(self, ctx, size):
        self._DrawCreature(ctx, 10, self._playerCreature)
        self._DrawCreature(ctx, 420, self._npcCreature)

    def _CheckCreatures(self):
        for _ in self._CheckDead():
            yield
        if self._playerCreature.IsDead():
            MenuFrame.Show(self._CreateSwitchMenu(), 'Next Victim', (20, 400), 16, 16)
            yield

        if self._npcCreature.IsDead() or not self._npcCreature in self._npc.creatures:
            # select a live npc creature
            for c in self._npc.creatures:
                if not c.IsDead():
                    self._npcCreature = c
                    DialogueFrame('The enemy switches in {0}!!!'.format(c.name)).Show()
                    yield

    def _CheckDead(self):
        if not self._npc.HasLiveCreature():
            DialogueFrame(self._winText).Show()
            yield
            self.KillSelf()
            self._winFunction()
            raise BattleEndError()

        if not self._player.HasLiveCreature():
            DialogueFrame(self._loseText).Show()
            yield
            self.KillSelf()
            self._loseFunction()
            while len(stateframe.stack) > 1:
                del stateframe.stack[-1] # back to main menu
            raise BattleEndError()


    def _CreateSwitchMenu(self):
        def DoSwitch(idx, c):
            self._playerCreature = c
            if c.name == 'Dog':
                DialogueFrame('Go, Dog. Go!').Show()
            else:
                DialogueFrame('Go {0}!!!'.format(c.name)).Show()
        return MakeCreatureMenu(self._player, DoSwitch,
                                lambda c: not c.IsDead() and c != self._playerCreature)
    
    def _CreateMenu(self):
        def DoPlayerAttack(attack):
            self._menuResult = self._playerCreature.AttackGenerator(attack, self._npcCreature, True)
            return False
            
        attacks = OrderedDict()
        for attack in self._playerCreature.attacks:
            attacks[attack.name] = lambda attack=attack : DoPlayerAttack(attack)

        def TryRun():
            DialogueFrame('You think about running, but decide that you are too lazy.').Show()
            return False

        def DoNothing():
            DialogueFrame('You quack some and try to fly.').Show()
            return False

        playerOptions = OrderedDict()
        playerOptions['Attack'] = attacks
        playerOptions['Use Item'] = InventoryFrame(self._player, npc=self._npc,
                                                   enemy=self._npcCreature)
        playerOptions['Switch Creatures'] = self._CreateSwitchMenu()
        playerOptions['Run Like a MOFO'] = TryRun
        playerOptions['Sit Like a Duck'] = DoNothing
        return playerOptions

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

        ctx.translate(0, HEALTH_HEIGHT + 50)
        sprite = Sprite(creature.name)

        spriteScale = (HEALTH_WIDTH - 10) / sprite.width
        ctx.translate(HEALTH_WIDTH / 2 - sprite.width * spriteScale / 2, 0)
        ctx.scale(spriteScale, spriteScale)
        sprite.Render(ctx)

        ctx.restore()

    def _NPCTurn(self):
        first = True
        while first or self._npcCreature.IsDead():
            first = False
            for _ in self._CheckCreatures():
                yield
            for msg in self._npcCreature.UpdateGenerator():
                DialogueFrame(msg).Show()
                yield
        
        move = self._npc.GetNextMove(self._npcCreature, self._playerCreature)
        story = list()
        if move[0] == 'attack':
            attack = move[1]
            for msg in self._npcCreature.AttackGenerator(attack, self._playerCreature):
                DialogueFrame(msg).Show()
                yield
        elif move[0] == 'item':
            DialogueFrame('Items do not work.').Show()
            yield 
        elif move[0] == 'switch':
            self._npcIndex = self._npc.creatures.index(move[1])
            DialogueFrame('The enemy switches creatures.').Show()
            yield
        else:
            DialogueFrame('The game is FULL of bugs. The NPC does nothing in protest.').Show()
            yield

    def _PlayerTurn(self):
        first = True
        while first or self._playerCreature.IsDead():
            first = False
            for _ in self._CheckCreatures():
                yield
            for msg in self._playerCreature.UpdateGenerator():
                DialogueFrame(msg).Show()
                yield

        self._menuResult = None
        MenuFrame.Show(self._CreateMenu(), 'What Now?', (20, 400), 16, 16)
        yield
        if self._menuResult is not None:
            for msg in self._menuResult:
                DialogueFrame(msg).Show()
                yield
        
    def _RunGame(self):
        npcName = 'A random ' + self._npc._sprite.name
        DialogueFrame([
                '{0} wants to fight!'.format(npcName),
                'You use {0}'.format(self._playerCreature.name),
                '{0} uses {1}'.format(npcName, self._npcCreature.name)
                ]).Show()
        yield

        if not (self._npc.HasLiveCreature() or self._player.HasLiveCreature()):
            DialogueFrame('BUG: Someone has no live creature').Show()
            yield
            exit(1)

        roundCount = 1
        try:                
            while True:
                # each round has two turns, player and npc
                DialogueFrame('Round {0}!'.format(roundCount)).Show()                    
                yield

                if self._playerCreature.speed >= self._npcCreature.speed:
                    DialogueFrame('You go first.').Show()
                    yield
                    toRun = [self._PlayerTurn(), self._NPCTurn()]
                else:
                    DialogueFrame('Your opponent goes first.').Show()
                    yield
                    toRun = [self._NPCTurn(), self._PlayerTurn()]

                for gen in toRun:
                    for _ in gen:
                        yield
                    for _ in self._CheckCreatures():
                        yield
                            
                roundCount += 1
        except BattleEndError:
            pass

def StartFight(player, npc):
    stateframe.stack.append(BattleFrame(player, npc, npc.winText, npc.loseText, npc.winFunction, npc.loseFunction))

if __name__ == '__main__':
    import board
    import entity
    import main
    from stateframe import FrameUpdate

    board = board.Board('test')
    player = entity.Player('hobo', (0,0), board)
    player.AddCreature(Creature('Dog'))
    player.AddCreature(Creature('Rat'))
    player.AddCreature(Creature('Programmer'))
    
    player.AddItem(entity.POSSIBLE_INVENTORY_ITEMS['spiked drink'][0])
    player.AddItem(entity.POSSIBLE_INVENTORY_ITEMS['thunderbird'][0])
    player.AddItem(entity.POSSIBLE_INVENTORY_ITEMS['thunderbird'][0])
    player.AddItem(entity.POSSIBLE_INVENTORY_ITEMS['speed'][0])

    npc = entity.NPC('hobo', (1,0), board)
    npc.AddCreature(Creature('Rat'))
    npc.AddCreature(Creature('Dog'))
    npc.AddCreature(Creature('Programmer'))
    npc.AddFightInfo('test win', 'test lose')

    StartFight(player, npc)
    win = main.Window('BattleFrame test')
    win.run(FrameUpdate)
