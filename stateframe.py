class StateFrame(object):
    def __init__(self, stack, input_processor, iterator, renderer):
        self.stack = stack
        self.inputProcessor = inputProcessor
        self.interator = iterator
        self.renderer = renderer

    def GetInput(input_dic):
        self.inputProcessor(input_dic)

    def Iterate():
        self.iterator()

    def Render(ctx, size):
        self.renderer(ctx, size)

    def KillSelf():
        stack.pop()
