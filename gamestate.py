stack = [] 

def InitGame():
    mainMenu = MainMenu()
    stack.append(mainMenu)

def FrameIterate():
    try:
        stack[-1].GetInput(GetInputState())
        stack[-1].Iterate()
        stack[-1].Render()
    finally:
        return stack
