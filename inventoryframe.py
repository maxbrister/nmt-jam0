from menuframe import MenuFrame
from graphics import *
class InventoryFrame(MenuFrame):
    def __init__(self, player, position = (20, 40), fontSizeTitle=50, fontSize=30, displayItems = None):

        self.player = player

        self.inventory = {}
        
        for item in player.inventory:
            self.inventory[item._name] = lambda : None
            
        if len(self.inventory) < 1 : 
            self.inventory["You don't even have lint..."] = lambda : None
        super(InventoryFrame, self).__init__(self.inventory, "Inventory", position, fontSizeTitle, fontSize, displayItems)

    def Render(self, ctx, size):
        super(InventoryFrame, self).Render(ctx, size)
        
        #ItemDesc = self.player.inventory[selected].GetDescription()
        itemDesc = "This is some item."

        DisplayTextBox(ctx, itemDesc, (300,40))
        
