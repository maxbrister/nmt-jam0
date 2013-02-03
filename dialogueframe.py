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
        self.currentDialogueLineIndex = 0

    def GetCurrentDialogue(self):
        for plotEvent in reversed(self._npc.dialogueList):
            if plotEvent == "" or self._player.plotEvents[plotEvent] == True:
                return self._npc.dialogueList[plotEvent]

    def PrintDialogue(self):
        print self.GetCurrentDialogue()[0]
                
    def Render(self, ctx, size):
        i = stack.index(self)
        if i > 0 :
            stack[i-1].Render(ctx, size)
        dialogue = self.GetCurrentDialogue()[0][self.currentDialogueLineIndex]
            
        DisplayTextBox(ctx, dialogue, (0,400), (800,200), 20, True)

        DisplayTextBox(ctx, "Press A to continue", (0,0), (180,20), 15)

    def GetInput(self, inputDict):
        if inputDict['a']:
            currentDialogueLine = self.GetCurrentDialogue()
            self.currentDialogueLineIndex += 1
            
            if(self.currentDialogueLineIndex >= len(currentDialogueLine[0])):
                self.EndDialogue();
                
        if inputDict['p'] or inputDict[chr(27)]:
            gametime.SetPlaying(False)
            stack.append(MenuFrame(boardframe.pause_menu, 'Pause'))

    def EndDialogue(self):
        endFunction = self.GetCurrentDialogue()[1]
        endFunction(self._player, self._npc)
        self.KillSelf()
    
