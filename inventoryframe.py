from menuframe import MenuFrame
from graphics import *
from collections import OrderedDict
class InventoryFrame(MenuFrame):
    def __init__(self, player, position = (20, 40), fontSizeTitle=50, fontSize=30, displayItems = None):

        self.player = player

        self.inventory = OrderedDict()

        itemIndex = 1
        for item in self.player.inventory:
            self.inventory[str(itemIndex) + '. ' + item._name] = lambda : None
            itemIndex += 1
            
        if len(self.inventory) < 1 : 
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

    
        
