from board import Board
from inputManager import UpdateInputEvent
from pygame.locals import *

stack = [] 
main_menu_list = ['Start Game', lambda : BoardFrame(stack), 'Exit', lambda : exit(0)]


def InitGame():
    mainMenu = MainMenuFrame(main_menu_list)
    stack.append(mainMenu)

def FrameUpdate(ctx,size):
    stack[-1].GetInput(UpdateInputEvent())
    if len(stack) == 0:
        return False
    stack[-1].Update()
    if len(stack) == 0:
        return False
    stack[-1].Render(ctx, size)
    return len(stack) > 0


class StateFrame(object):
    def __init__(self):
        pass

    def GetInput(self, inputDic):
        # subclass should override
        pass

    def Update(self):
        # subclass should override
        pass

    def Render(self, ctx, size):
        # subclass should override
        pass

    def KillSelf(self):
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
    def __init__(self, options):
        super(MainMenuFrame, self).__init__()
        self.options = options
        self.selected = 0

    def Render(self, ctx, size):
        for option in self.options:
            print option[0]

        print '*** %s' % (self.options[self.selected][0])

    def GetInput(self, input_dict):
        if input_dict['w']:
            self.selected = (self.selected - 1) % len(self.options)
        if input_dict['s']:
            self.selected = (self.selected + 1) % len(self.options)
        if input_dict['a']:        #I have no idea how to handle enter...
            if isinstance(self.options[self.selected][1], list):
                stack.append(MainMenuFrame(self.options[self.selected][1]))
            else:
                stack.append(self.options[self.selected][1]())

class BoardFrame(StateFrame):
    def __init__(self, boardName='test'):
        super(BoardFrame, self).__init__()
        self._board = Board(boardName)

    def Render(self, ctx, size):
        self._board.Render(ctx)

if __name__ == '__main__':
    import main
    
    # test BoardFrame
    stack.append(BoardFrame())
    win = main.Window('BoardFrame Test')
    win.run(FrameUpdate)
