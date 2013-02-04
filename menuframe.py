from graphics import RenderMenu
from stateframe import StateFrame, stack
from math import ceil, floor

class MenuFrame(StateFrame):

    @staticmethod
    def Show(options, title=None, position = (20, 40), fontSizeTitle=50, fontSize=30, displayItems = None):
        frame = MenuFrame(options, title, position, fontSizeTitle, fontSize, displayItems)
        stack.append(frame)

    def __init__(self, options, title=None, position = (20, 40), fontSizeTitle=50, fontSize=30, displayItems = None):
        super(StateFrame, self).__init__()
        self.inputMode='Discrete'
        self.options = options        #{'title':function/submenu list}
        self.selected = 0
        self.title = title
        self.position = position
        self.fontSizeTitle = fontSizeTitle
        self.fontSize = fontSize
        
        if displayItems is None:
            self.displayItems = len(options)
        else:
            self.displayItems = displayItems
            
        self.displayRange = [0, self.displayItems]


    def Render(self, ctx, size):
        i = stack.index(self)
        while i>0 and isinstance(stack[i-1], MenuFrame):
            i -= 1
        if i > 0 :
            stack[i-1].Render(ctx, size)
        RenderMenu(ctx, self.title, self.options.keys()[self.displayRange[0]:self.displayRange[1]], self.selected-self.displayRange[0], self.position, self.fontSizeTitle, self.fontSize)
        
    
    def GetInput(self, input_dict):
        if input_dict['w']:
            self.selected = (self.selected - 1) % len(self.options)
            self.UpdateDisplayRange()
        if input_dict['s']:
            self.selected = (self.selected + 1) % len(self.options)
            self.UpdateDisplayRange()
            
        if input_dict['a']:        #I have no idea how to handle enter...
            keySelected = self.options.keys()[self.selected]
            valueSelected = self.options.values()[self.selected]
            self._ResolveSelection(keySelected, valueSelected)
        
    def UpdateDisplayRange(self):
        if(self.selected <= self.displayItems - 1):
            self.displayRange = [0, self.displayItems]
        elif(self.selected >= len(self.options) - (self.displayItems-1)):
            self.displayRange = [len(self.options) - self.displayItems, len(self.options)]
        else:
            self.displayRange[0] = self.selected - int(ceil(self.displayItems/2))
            self.displayRange[1] = self.selected + int(floor(self.displayItems/2))

    def _ResolveSelection(self, keySelected, valueSelected):
        if isinstance(valueSelected, dict):
            stack.append(MenuFrame(valueSelected, keySelected, self.position, self.fontSizeTitle, self.fontSize,
                                   self.displayItems))
        elif isinstance(valueSelected, StateFrame):
            stack.append(valueSelected)
        else:
            try:
                output = valueSelected()
                self._ResolveSelection(keySelected, output)
            except TypeError:
                if not valueSelected:
                    while len(stack) > 1 and isinstance(stack[-1], MenuFrame):
                        stack[-1].KillSelf()
