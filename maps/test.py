def Initialize(entity, board):
    ent0 = entity.NPC('foo', (5, 5), board)
    ent0.AddToDialogueList('foo', 'Hello World!')
    
    ent1 = entity.NPC('beer', [(2, 3), (6, 3), (6, 6), (2, 6)], board)
    ent1.AddToDialogueList('bar', 'You should really take your medication.')
