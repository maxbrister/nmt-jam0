from inputManager import UpdateInputEvent
from stateframe import BoardFrame

stack = [] 
main_menu_list = ['Start Game', lambda : BoardFrame(stack), 'Exit', lambda : exit(0)]


def InitGame():
    mainMenu = MainMenuFrame(stack, main_menu_list)
    stack.append(mainMenu)

def FrameUpdate(ctx,size):
    try:
        stack[-1].GetInput(GetInputState())
        stack[-1].Update()
        stack[-1].Render(ctx, size)

    except Error as e:
        print str(e)

    finally:
        return stack
