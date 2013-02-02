from inputManager import UpdateInputEvent

stack = [] 
main_menu_list = []


def InitGame():
#    mainMenu = MainMenuFrame(stack, main_menu_list)
#    stack.append(mainMenu)
    stack.append(1)

def FrameUpdate(ctx,size):
    try:
        stack[-1].UpdateInputEvent(GetInputState())
        stack[-1].Update()
        stack[-1].Render(ctx, size)

    except Error as e:
        print str(e)

    finally:
        return stack
