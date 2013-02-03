from stateframe import *
from main import *
from entity import Player
import collections
import gametime
from menuframe import MenuFrame
import boardframe
from graphics import DisplayTextBox

class DialogueFrame(StateFrame):

    FONTSIZE = 20
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 800


    def __init__(self, player, npc):
        super(DialogueFrame, self).__init__()
        self._player = player
        self._npc = npc

    def GetCurrentDialogue(self):
        
        for plotEvent in reversed(self._npc.dialogueList):
            if self._player.plotEvents[plotEvent] == True:
                return self._npc.dialogueList[plotEvent]

    def PrintDialogue(self):
        print self.GetCurrentDialogue()[0]
                
    def Render(self, ctx, size):
        i = stack.index(self)
        if i > 0 :
            stack[i-1].Render(ctx, size)
        
        dialogue = self.GetCurrentDialogue()[0]
        
        DisplayTextBox(ctx, dialogue, (0,400), (800,200), 20, True)

        DisplayTextBox(ctx, "Press A to continue", (0,0), (180,20), 15)

    def GetInput(self, inputDict):
        if inputDict['a']:
            endFunction = self.GetCurrentDialogue()[1]
            endFunction(self._player, self._npc)
            self.KillSelf()
            
        if inputDict['p'] or inputDict[chr(27)]
            gametime.SetPlaying(False)
            stack.append(MenuFrame(boardframe.pause_menu, 'Pause'))

                
#remade from the entity version of NPC for testing
class NPC2(object):
    def __init__(self):
        #dictionary of dialogue texts keyed by plot events
        self.dialogueList = collections.OrderedDict()

    #add a named plot event with dialogue text to this npc
    def AddToDialogueList(self, plotEvent, dialogueTextList, endFunction = lambda player, npc:None):
        self.dialogueList[plotEvent] = (dialogueTextList, endFunction)
        self._endFunction = endFunction


if __name__ == '__main__':

    import board
    board = board.Board("test")
    
    player = Player("foo", (0,0), board)
    npc = NPC2()
    
    frame = DialogueFrame(player, npc)

    player.AddPlotEvent("testEvent")
    player.AddPlotEvent("testEvent2")
    def functionA(player, npc):
        print "HI"
        
    npc.AddToDialogueList("testEvent", "hi", functionA)
    npc.AddToDialogueList("testEvent2", "012345678901234567890123456789", functionA)
    
    player.FinishPlotEvent("testEvent")
    frame.PrintDialogue()
    player.FinishPlotEvent("testEvent2")
    frame.PrintDialogue()

    stack.append(frame)
    win = Window('Dialogue Frame')
    win.run(FrameUpdate)
