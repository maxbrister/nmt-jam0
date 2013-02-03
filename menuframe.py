from graphics import RenderMenu
from stateframe import StateFrame, stack

class MenuFrame(StateFrame):
    def __init__(self, options):
        super(StateFrame, self).__init__()
        self.inputMode='Discrete'
        self.options = options        #{'title':function/submenu list}
        self.selected = 0
        self.title = 'TEST TITLE YO!'

    def Render(self, ctx, size):
        i = stack.index(self)
        if i > 0:
            stack[i-1].Render()

    def GetInput(self, input_dict):
        if input_dict['w']:
            self.selected = (self.selected - 1) % len(self.options)
        if input_dict['s']:
            self.selected = (self.selected + 1) % len(self.options)
        if input_dict['a']:        #I have no idea how to handle enter...
            if isinstance(self.options[self.selected][1], dict):
                stack.append(MenuFrame(self.options[self.selected][1]))
            else:
                stack.append(self.options[self.selected][1]())


class MainMenuFrame(MenuFrame):
    def Render(self, ctx, size):
        RenderMenu(ctx, self.title, self.options.keys(), self.selected)

    def GetInput(self, input_dict):
        if input_dict['w']:
            self.selected = (self.selected - 1) % len(self.options)
        if input_dict['s']:
            self.selected = (self.selected + 1) % len(self.options)
        if input_dict['a']:        #I have no idea how to handle enter...
            if isinstance(self.options[self.selected][1], dict):
                stack.append(MainMenuFrame(self.options[self.selected][1]))
            else:
                stack.append(self.options[self.selected][1]())


class BattleMenuFrame(MenuFrame):
    pass

class PauseMenuFrame(MenuFrame):
    pass
