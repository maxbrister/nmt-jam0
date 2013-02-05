import creature
import collections
import dialogueframe
import graphics
import menuframe

from creature import MakeCreatureMenu
from collections import OrderedDict
from dialogueframe import DialogueFrame
from graphics import *
from menuframe import MenuFrame


class InventoryFrame(MenuFrame):
    def __init__(self, player, position = (20, 40), fontSizeTitle=50, fontSize=30, displayItems = None,
                 npc = None, enemy = None):

        self.player = player
        self.npc = npc
        self.enemy = enemy

        self.onSelectOther = None
        self._UpdateMenu()
        super(InventoryFrame, self).__init__(self.options, "Inventory", position, fontSizeTitle, fontSize, displayItems)

    @property
    def item(self):
        return self.player.inventory[self.selected]

    def Render(self, ctx, size):
        super(InventoryFrame, self).Render(ctx, size)
        if self.selected < len(self.player.inventory):
            itemDesc = self.player.inventory[self.selected].description
        else:
            itemDesc = "You are a poor homeless individual"

        DisplayTextBox(ctx, itemDesc, (400,40), (400, None))

        playermoney = str(self.player._money) + " cents"
        
        DisplayTextBox(ctx, playermoney, (10, 560))

    def _DropItem(self):
        self.player.RemoveItem(self.selected)
        self._UpdateMenu()

    def _ResolveSelection(self, keySelected, valueSelected):
        if valueSelected == 'back':
            super(InventoryFrame, self)._ResolveSelection(keySelected, valueSelected)
        else:
            if self.item.target == 'friendly':
                # select someone to use the item on
                useMenu = MakeCreatureMenu(self.player, lambda _, c: self._UseItem(c), hasBack=True)
                useTitle = 'Use {0}'.format(self.item.name)
                if self.enemy is None:
                    options = OrderedDict()
                    if len(self.player.creatures) > 0:
                        options[useTitle] = useMenu
                    options['Drop'] = self._DropItem
                    options['Back'] = 'back'
                    super(InventoryFrame, self)._ResolveSelection(keySelected, options)
                else:
                    super(InventoryFrame, self)._ResolveSelection(useTitle, useMenu)
            elif self.item.target == 'enemy':
                if self.enemy is None:
                    options = OrderedDict()
                    options['Drop'] = self._DropItem
                    options['Back'] = 'back'
                    super(InventoryFrame, self)._ResolveSelection(keySelected, options)
                else:
                    self._UseItem(self.enemy)
                    super(InventoryFrame, self)._ResolveSelection(keySelected, False)
            else:
                raise Exception('Unrecognized item target: ' + self.item.target)

    def _UpdateMenu(self):
        self.options = OrderedDict()

        for itemIndex, item in enumerate(self.player.inventory):
            self.options[str(itemIndex+1) + '. ' + item.name] = None
        
        self.empty = len(self.player.inventory) < 1
        if self.empty:
            self.options["A pocketful of wishes"] = 'back'
        else:
            self.options['Back'] = 'back'
        
    def _UseItem(self, creature):
        msg = self.item.Apply(creature, True, self.player, self.npc)
        self._DropItem()
        DialogueFrame(msg).Show()

if __name__ == '__main__':
    import board
    import entity
    import main
    import stateframe

    from stateframe import FrameUpdate, stack

    board = board.Board('test')
    player = entity.Player('hobo', (0,0), board)
    player.AddCreature
    player.AddItem(entity.POSSIBLE_INVENTORY_ITEMS['spiked drink'][0])
    player.AddItem(entity.POSSIBLE_INVENTORY_ITEMS['thunderbird'][0])
    player.AddItem(entity.POSSIBLE_INVENTORY_ITEMS['thunderbird'][0])
    player.AddItem(entity.POSSIBLE_INVENTORY_ITEMS['speed'][0])

    stack.append(InventoryFrame(player))
    win = main.Window('ItemFrame test')
    win.run(FrameUpdate)
    
