def Initialize(entity, board):
    ent0 = entity.NPC('blind', (6, 6), board)
    ent0.AddToDialogueList('foo', 'Change for a dying man?',lambda player,npc:player.FinishPlotEvent('talktoblind'))
    #ent0.AddToDialogueList('foo', 'Oh.  I see.  Nevermind.')
    #ent0.AddToDialogueList('foo', 'I am an old man, and do not have long left.  Will you listen?')
    #ent0.AddToDialogueList('foo', 'Among the street people, there is a story, told in whispers in the dark.')
    
    ent1 = entity.NPC('beer', [(2, 3), (4, 3), (4, 4), (2, 4)], board)
    ent1.AddToDialogueList('foo', 'You should really take your medication.')

    ent2 = entity.NPC('hookerii', (1, 11), board)
    ent2.AddToDialogueList('foo', 'Bitch be trippin.')
    ent2.AddToDialogueList('talktoblind', 'Don\'t make me thump you.')

    ent3 = entity.NPC('piletrash', (5, 6), board)
    ent3.AddToDialogueList('foo', 'A pile of trash.  You think you see a banana.')

    ent4 = entity.NPC('piletrash', (11, 2), board)
    ent3.AddToDialogueList('foo', 'A pile of trash.  Smells a bit like pee.')

    ent5 = entity.NPC('traffsh', (10, 3), board)
    ent3.AddToDialogueList('foo', 'A broken car, with an angry man living inside.')

    ent6 = entity.NPC('traffsh', (11, 4), board)
    ent3.AddToDialogueList('foo', 'A broken car full of feral cats.')

    ent7 = entity.NPC('hipster', (20, 0), board)
    ent3.AddToDialogueList('foo', 'Smells like niche music.')
    ent8 = entity.NPC('postbox', (10, 0), board)
    ent3.AddToDialogueList('foo', 'You got your hand stuck in one of those once.')


    #trashcan = entity.Container('trashcan', (3,8), board)
