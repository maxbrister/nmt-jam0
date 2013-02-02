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


