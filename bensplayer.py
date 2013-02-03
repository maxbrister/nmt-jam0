class Player(object):
    def __init__(self):
        self._creatures = (Creature("Programmer"), Creature("Black Woman"))
        self._currentCreature = 0

    #dictionary of plot events and whether they have been finished/accomplished
    plotEvents = {}

    #add a named plot event to the player
    def AddPlotEvent(self, name):
        self.plotEvents[name] = False;

    #make the player 'accomplish' a plot event
    def FinishPlotEvent(self, name):
        self.plotEvents[name] = True;
        
    def GetCurrentCreature(self):
        return self._currentCreature

    def SetCurrentCreature(self, creatureIndex):
        pass