from inputManager import GetInputEvent

stack = [] 

def InitGame():
    #mainMenu = MainMenu()
    #stack.append(mainMenu)
    stack.append(1)

def FrameIterate():
    try:
        stack[-1].GetInput(GetInputState())
        stack[-1].Update()
        stack[-1].Render()

    except Error as e:
        print str(e)

    finally:
        return stack
