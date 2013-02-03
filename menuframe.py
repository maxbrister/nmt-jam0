from graphics import RenderMenu
from stateframe import StateFrame, stack

class MenuFrame(StateFrame):
    def __init__(self, options, title=None, position = (20, 40)):
        super(StateFrame, self).__init__()
        self.inputMode='Discrete'
        self.options = options        #{'title':function/submenu list}
        self.selected = 0
        self.title = title
        self.position = position

    def Render(self, ctx, size):
        i = stack.index(self)
        while i>0 and isinstance(stack[i-1], MenuFrame):
            i -= 1
        if i > 0 :
            stack[i-1].Render(ctx, size)
        RenderMenu(ctx, self.title, self.options.keys(), self.selected, self.position)


    def GetInput(self, input_dict):
        if input_dict['w']:
            self.selected = (self.selected - 1) % len(self.options)
        if input_dict['s']:
            self.selected = (self.selected + 1) % len(self.options)
        if input_dict['a']:        #I have no idea how to handle enter...
            if isinstance(self.options[self.options.keys()[self.selected]], dict):
                stack.append(MenuFrame(self.options[self.options.keys()[self.selected]], self.options.keys()[self.selected]))
            else:
                output = self.options[self.options.keys()[self.selected]]()
                if isinstance(output, StateFrame):
                    stack.append(output)
                elif not output:
                    self.KillSelf()

class BattleMenuFrame(MenuFrame):
    pass
