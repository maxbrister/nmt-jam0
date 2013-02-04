import creature
import collections
import graphics
import menuframe

from creature import MakeCreatureMenu
from collections import OrderedDict
from graphics import *
from menuframe import MenuFrame


class InventoryFrame(MenuFrame):
    def __init__(self, player, position = (20, 40), fontSizeTitle=50, fontSize=30, displayItems = None,
                 enemy = None):

        self.player = player

        self.inventory = OrderedDict()

        self.onSelectOther = None
        self.onFinish = None

        for itemIndex, item in enumerate(self.player.inventory):
            self.inventory[str(itemIndex+1) + '. ' + item._name] = lambda : None

        self.empty = len(self.inventory) < 1
        if self.empty:
            self.inventory["A pocketful of wishes"] = lambda : None
            
        super(InventoryFrame, self).__init__(self.inventory, "Inventory", position, fontSizeTitle, fontSize, displayItems)
        

    def Render(self, ctx, size):
        super(InventoryFrame, self).Render(ctx, size)
        if len(self.player.inventory) >= 1:
            ItemDesc = self.player.inventory[self.selected].GetDescription()
        else:
            ItemDesc = "You are a poor homeless individual"
        #itemDesc = "This is some item."

        DisplayTextBox(ctx, ItemDesc, (400,40), (400, None))

        playermoney = str(self.player._money) + " cents"
        
        DisplayTextBox(ctx, playermoney, (10, 560)) 

    def _ResolveSelection(self, keySelected, valueSelected):
        if self.empty:
            if self.onFinish is None:
                super(InventoryFrame, self)._ResolveSelection(keySelected, valueSelected)
            else:
                self.onFinish(-1)
        else:
            item = self.player.inventory[self.selected]
            if item.target == 'friendly':
                # select someone to use the item on
                options = OrderedDict()
                options['Use'] = MakeCreatureMenu(self.player, lambda _, c: self._UseItem(c))
                super(InventoryFrame, self)._ResolveSelection(keySelected, options)
                
    def _UseItem(self, creature):
        item = self.player.inventory[self.selected]
        item.Apply(creature, True, player)
        
