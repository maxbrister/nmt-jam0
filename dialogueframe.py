from stateframe import StateFrame
from main import *
from bensplayer import*
class DialogueFrame(StateFrame):
    def __init__(self, player, npc):
        self._player = player
        self._npc = npc

    def PrintDialogue(self):
        for plotEvent in self._npc.dialogueList:
            if self._player.plotEvents[plotEvent] == True:
                print self._npc.dialogueList[plotEvent]

    def Render(self, ctx, size):
        pass

                
#remade from the entity version of NPC for testing
class NPC(object):
    def __init__(self):
        #dictionary of dialogue texts keyed by plot events
        self.dialogueList = {}

    #add a named plot event with dialogue text to this npc
    def AddToDialogueList(self, plotEvent, dialogueText):
        self.dialogueList[plotEvent] = dialogueText


if __name__ == '__main__':

    player = Player()
    npc = NPC()
    
    frame = DialogueFrame(player, npc)

    player.AddPlotEvent("testEvent")
    player.AddPlotEvent("testEvent2")

    npc.AddToDialogueList("testEvent", "BLA BLA BLA OBAMACARE")
    npc.AddToDialogueList("testEvent2", "BLA BLA OIL SNAKE HEADED ALIENS")

    player.FinishPlotEvent("testEvent")
    frame.PrintDialogue()
    player.FinishPlotEvent("testEvent2")
    frame.PrintDialogue()
