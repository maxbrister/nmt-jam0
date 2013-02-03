def Initialize(entity, board):
    ent0 = entity.NPC('foo', (5, 5), board)
    ent0.AddToDialogueList('foo', 'Hello World!')
    
    ent1 = entity.NPC('bar', [(1, 1), (1, 10), (10, 10), (10, 1)], board)
    ent1.AddToDialogueList('foo', 'GRRRRRRRRR')
