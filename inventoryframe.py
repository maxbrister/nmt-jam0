from menuframe import MenuFrame
from graphics import *
from collections import OrderedDict
class InventoryFrame(MenuFrame):
    def __init__(self, player, position = (20, 40), fontSizeTitle=50, fontSize=30, displayItems = None):

        self.player = player

        self.inventory = OrderedDict()
        
        for item in player.inventory:
            self.inventory[item._name] = lambda : None
            
        if len(self.inventory) < 1 : 
            self.inventory["You don't even have lint..."] = lambda : None
        super(InventoryFrame, self).__init__(self.inventory, "Inventory", position, fontSizeTitle, fontSize, displayItems)
        

    def Render(self, ctx, size):
        super(InventoryFrame, self).Render(ctx, size)
        print self.player.inventory
        if len(self.player.inventory) >= 1:
            ItemDesc = self.player.inventory[self.selected].GetDescription()
        else:
            ItemDesc = "You are a poor homeless individual"
        #itemDesc = "This is some item."

        DisplayTextBox(ctx, ItemDesc, (300,40))

    
        
