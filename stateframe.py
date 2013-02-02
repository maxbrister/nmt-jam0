from pygame.locals import *

class StateFrame(object):
    def __init__(self, stack, input_processor, updater, renderer):
        self.stack = stack
        self.inputProcessor = inputProcessor
        self.interator = iterator
        self.renderer = renderer

    def GetInput(input_dic):
        self.inputProcessor(input_dic)

    def Update():
        self.updater()

    def Render(ctx, size):
        self.renderer(ctx, size)

    def KillSelf():
        stack.pop()


'''
Options = [('name', element)]
where if element is a list, sub-menu
otherwise, it is a function. This function will
always be appended to the stack frame, for convenience.

By the way, we need global game shit... like a player?
And a board?

YEah... things, man...

I forgot to add menu titles. I can take care of that later.
'''
class MainMenuFrame(StateFrame):
    def __init__(self, stack, options):
        super(MainMenu, self).__init__(
            stack, self.Inputprocessor, self.Updater, self.Renderer)
        self.options = options
        self.selected = 0

    def Updater():
        pass

    def Renderer(ctx, size):
        for option in self.options:
            print option[0]

        print '*** %s' % (self.options[self.selected][0]

    def InputProcessor(input_dict):
        if input_dict['w']:
            self.selected = (self.selected - 1) % len(self.options)
        if input_dict['s']:
            self.selected = (self.selected + 1) % len(self.options)
        if input_dict['a']:        #I have no idea how to handle enter...
            if isinstance(self.options[self.selected][1], list):
                self.stack.append(MainMenuFrame(self.options[self.selected][1]))
            else:
                self.stack.append(self.options[self.selected][1]())
