class Player(object):
    def __init__(self):
        self._creatures = (Creature("Programmer"), Creature("Black Woman"))
        self._currentCreature = 0

    def GetCurrentCreature(self):
        return self._currentCreature

    def SetCurrentCreature(self, creatureIndex):
        pass
