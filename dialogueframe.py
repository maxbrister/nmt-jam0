from stateframe import StateFrame

class DialogueFrame(StateFrame):
    def __init__(self, player, npc):
        self._player = player
        self._npc = npc

    def PrintDialogue(self):
        for plotEvent in self._npc.dialogueList:
            if self._player.plotEvents[plotEvent] == True:
                print self._npc.dialogueList[plotEvent]
        

class NPC(object):
    def __init__(self):
        #dictionary of dialogue texts keyed by plot events
        self.dialogueList = {}

    #add a named plot event with dialogue text to this npc
    def AddToDialogueList(self, plotEvent, dialogueText):
        self.dialogueList[plotEvent] = dialogueText
