from stateframe import StateFrame, stack
from main import *
from bensplayer import*
import re
class DialogueFrame(StateFrame):

    FONTSIZE = 20
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 800
    

    def __init__(self, player, npc):
        super(DialogueFrame, self).__init__()
        self._player = player
        self._npc = npc

    def PrintDialogue(self):
        for plotEvent in self._npc.dialogueList:
            if self._player.plotEvents[plotEvent] == True:
                print self._npc.dialogueList[plotEvent]
                
    def GetDialogueString(self):
        dialogueString = ""
        for plotEvent in self._npc.dialogueList:
            if self._player.plotEvents[plotEvent] == True:
                dialogueString += self._npc.dialogueList[plotEvent]
        #print dialogueString

        #make sure that the text doesnt start with a space
        if dialogueString[0] == " ":
            dialogueString = dialogueString[1:]
        
        #split the text every characters
        dialogueText = []
        every = 70
        for i in xrange(0, len(dialogueString), every):
            dialogueText.append(dialogueString[i:i+every])

        #I'm aware the following is silly.
        for x in range(0, len(dialogueText)):
            #if the line doesnt end with a space, add a dash
            if dialogueText[x][-1] != " ":
                dialogueText[x] += "-"

            #remove dash from previous line if this line begins with a space
            if dialogueText[x][0] == " ":
                dialogueText[x-1] = dialogueText[x-1][:-1]
                dialogueText[x] = dialogueText[x][1:]

        #remove dash from very end of text
        dialogueText[-1] = dialogueText[-1][:-1]

        return dialogueText
                
    def Render(self, ctx, size):
        dialogue = self.GetDialogueString()
        textHeight = self.FONTSIZE*len(dialogue)
        
        ctx.rectangle(0, self.SCREEN_HEIGHT - (textHeight + self.FONTSIZE), self.SCREEN_WIDTH, textHeight + self.FONTSIZE)
        ctx.set_source_rgb(0.5,0.5,0.5)
        ctx.fill()
        for line in dialogue:
            self.WriteText(ctx, size, (10,self.SCREEN_HEIGHT - textHeight), line)
            textHeight -= self.FONTSIZE
        
        
    def WriteText(self, ctx, size, location, text):
        ctx.select_font_face('monospace')
        ctx.move_to(location[0], location[1])
        ctx.set_font_size(self.FONTSIZE)
        ctx.text_path(text)
        ctx.set_source_rgb(1,1,1)
        ctx.stroke()

                
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

    npc.AddToDialogueList("testEvent", "Lorem ipsum dolor amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    npc.AddToDialogueList("testEvent2", "012345678901234567890123456789")

    player.FinishPlotEvent("testEvent")
    frame.PrintDialogue()
    player.FinishPlotEvent("testEvent2")
    frame.PrintDialogue()

    stack.append(frame)
    win = Window('Dialogue Frame')
    win.run(FrameUpdate)
