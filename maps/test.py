def Initialize(entity, board):
    ent0 = entity.NPC('hobo', (6, 6), board)
    ent0.AddToDialogueList('foo', 'Change for a dying man?')
    ent0.AddToDialogueList('foo', 'Oh.  I see.  Nevermind.')
    ent0.AddToDialogueList('foo', 'I am an old man, and do not have long left.  Will you listen?')
    ent0.AddToDialogueList('foo', 'Among the street people, there is a story, told in whispers in the dark.')



    
    ent1 = entity.NPC('beer', [(2, 3), (6, 3), (6, 6), (2, 6)], board)
    ent1.AddToDialogueList('foo', 'You should really take your medication.')
