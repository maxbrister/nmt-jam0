import collections
from collections import OrderedDict

def MakeEntity(NPCS, name, sprite, X,Y, animals, dialog):
    #make the entity
    NPCS.append(entity.NPC(sprite, (X,Y), board)
    #get dialog/event pairs, and add them to the text
    for sentence in dialog:
        sentence = sentence.split('=')
    if len(sentence) =
    NPCS[len(NPCS)].
    print name, sprite, X, Y,
    print animals
    print dialog

#import entities
try:
    dat = open(("ents.ent"))
    lines = dat.readlines()
except IOError:
        raise EntityError('importing entities failed')
entities = "".join(lines)
lines = entities.split("\n")
NPCS = []

for line in lines:
    if line:
        temp = line.split('#')
        #get list of animal names
        animals = []
        list2 = temp[0]
        list2 = temp[0].split('|')
        for animal in list2:
            animals.append(animal)
        #get list of dialog choices
        dialog = []
        list3 = temp[1]
        list3 = temp[1].split('|')
        for sentence in list3:
            dialog.append(sentence)
        #get the basic information
        temp1 = temp[2].split(',')
        name = temp1[2]
        sprite = temp1[1]
        X = temp1[2]
        Y = temp1[3]
        MakeEntity(NPCS, name, sprite, X, Y, animals, dialog)
    
    



                          


