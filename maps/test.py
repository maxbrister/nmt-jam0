def Initialize(entity, board):
    ent0 = entity.NPC("blind", (6, 6), board)
    ent0dialog = ["Change for a dying man?", "Oh, I see.  Nevermind.", "Well, so long as you are here, why don\'t you make yourself useful and hear an old man\'s story?", "One time event only.  Last show.  Venue closing.", "I was a young man like you, once.", "Young and full of hope that one day, maybe, I might sleep in a bed that didn\'t smell of pee.", "But there is a darker path, too.", "And those who take it are spoken of in whispers in the dark, among the people in the street.", "I was destroyed, body and soul, by one of them.  He calls himself the king.", "Here.  Take my friend and protector.  You won't last long without him, and I have so very little - time - left..."]    
    ent0.AddToDialogueList('foo', ent0dialog,lambda player,npc:player.FinishPlotEvent("talktoblind"))
    
    ent1 = entity.NPC('beer', [(2, 3), (4, 3), (4, 4), (2, 4)], board)
    ent1DialogueList = ["You should really take your medication.", "Or integrate your ears with respect to pidgeon. Whatever."]
    ent1.AddToDialogueList('foo', ent1DialogueList)

    ent2 = entity.NPC('hookerii', (1, 11), board)

    ent2.AddToDialogueList('foo', ["Bitch be trippin."])
    ent2.AddToDialogueList('talktoblind', ["I know your kind.  You just get back on that bus and leave.", "Don\'t you make me fight your homeless ass."])

    ent3 = entity.NPC('piletrash', (5, 6), board)
    ent3.AddToDialogueList("foo", ["A pile of trash.  You think you see a banana."])

    ent4 = entity.NPC('piletrash', (11, 0), board)
    ent4.AddToDialogueList("foo", ["A pile of trash.  Smells a bit like pee."])

    ent5 = entity.NPC('traffsh', (10, 3), board)
    ent5.AddToDialogueList('foo', ["An abandoned car."])

    ent6 = entity.NPC('traffsh', (11, 4), board)
    ent6.AddToDialogueList('foo', ["A broken car full of feral cats."])

    ent7 = entity.NPC('hipster', (20, 0), board)
    ent7.AddToDialogueList('foo', ["Smells like niche music."])

    ent8 = entity.NPC('postbox', (10, 0), board)
    ent8.AddToDialogueList('foo', ["You got your hand stuck in one of those once."])
	
    ent9 = entity.NPC('traffsh', (0, 8), board)
    ent9.AddToDialogueList('foo', ["A lone car, abandoned in a parking lot.  Sends a shiver down your spine.  But maybe that\'s just the DT\'s..."])	

    ent10 = entity.NPC('Doc', (11,6), board)
    ent10.AddToDialogueList('foo', ["Hey.  Come here.  Vant to buy organs?", "I vill fix your animals.  New parts!  Better parts!", "Of course I have license!  How dare you question qualifications?"])	

    ent11 = entity.NPC('crowd', (11,2), board)
    ent11.AddToDialogueList('foo', ["Rabble rabble rabble"])	


    trashcan = entity.Container('trashcan', (9,0), board)
    dumpster0 = entity.Container('Dumpster', (4,6), board)

    dumpster1 = entity.Container('Dumpster', (15,9), board)
    dumpster2 = entity.Container('Dumpster', (16,9), board)
    dumpster3 = entity.Container('Dumpster', (17,9), board)
