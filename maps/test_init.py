import collections
from collections import OrderedDict
def Initialize(menuframe, battle, creature, entity, board, entities, containers):
    def TalkBlind(player, npc):
        player.FinishPlotEvent('talktoblind')
        options = OrderedDict()
        options['Cockroach'] = lambda : addanimal(player, 'Cockroach')
        options['Rat'] = lambda : addanimal(player, 'Rat')
        options['Racoon'] = lambda : addanimal(player, 'Racoon')
        menuframe.MenuFrame.Show(options, 'Quickly!  Choose before the police show up.')

    def addanimal(player, option):
        player.AddCreature(creature.Creature(option))
    entities['blind'].FinishDialouge('foo', TalkBlind)


    def OnHookerFinish(hooker):
        hooker.path = [(1, 22)]
    hooker = entities['Random Hooker']
    hooker.FinishFight(lambda: OnHookerFinish(hooker))
