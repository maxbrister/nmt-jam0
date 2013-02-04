import collections
import entity
import graphics
import menuframe
import stateframe

from entity import Player
from graphics import DisplayTextBox
from menuframe import MenuFrame
from stateframe import StateFrame, stack

class NoDialogueError(Exception):
    def __init__(self, npc):
        self.msg = 'Lack of dialog options for ' + npc.name

    def __str__(self):
        return self.msg

class DialogueFrame(StateFrame):

    FONTSIZE = 20
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 800

    @staticmethod
    def ForPlayer(player, npc, show=True):
        for plotEvent in reversed(npc.dialogueList):
            if not plotEvent or player.plotEvents[plotEvent]:
                ret = DialogueFrame(npc.dialogueList[plotEvent][0],
                                    lambda player=player, npc=npc: npc.dialogueList[plotEvent][1](player, npc))
                if show:
                    ret.Show()
                return ret
        raise NoDialogueError(npc)

    
    def __init__(self, dialogueList, endFunction = lambda: None, showAccept=False):
        super(DialogueFrame, self).__init__()

        # dialogueList can be a single string
        try:
            dialogueList[0][0]
        except TypeError:
            dialogueList = [dialogueList]

        assert len(dialogueList) > 0
        
        self.dialogueList = dialogueList
        self.showAccept = showAccept
        self.endFunction = endFunction
        self.currentDialogueLineIndex = 0

    @property
    def currentDialogue(self):
        return self.dialogueList[self.currentDialogueLineIndex]
                
    def Render(self, ctx, size):
        self.RenderParent(ctx, size)
        DisplayTextBox(ctx, self.currentDialogue, (0,400), (800,200), 20, True)
        if self.showAccept:
            DisplayTextBox(ctx, "Press A to continue", (0,0), (180,20), 15)

    def GetInput(self, inputDict):
        if inputDict['a']:
            self.currentDialogueLineIndex += 1
            if(self.currentDialogueLineIndex >= len(self.dialogueList)):
                self.EndDialogue()
                
    def EndDialogue(self):
        self.KillSelf()
        self.endFunction()
    
