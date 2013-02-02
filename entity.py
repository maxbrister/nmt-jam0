class Entity:
    __SpriteStill = None
    __SpriteMoveUp = None
    __SpriteMoveDown = None
    __SpriteMoveLeft = None
    __SpriteMoveRight = None
    __Position = None

    """
    " @SpriteStill the basic sprite, if no other sprites are defined this one is used
    " @Position a dictionary {x: val, y: val}
    " @SpriteMoveUp the sprite used when the entity moves up
    "     The other movement sprites default to this if not defined (and SpriteMoveRight is not defined)
    " @SpriteMoveRight the sprite used when the entity moves right
    "     SpriteMoveLeft defaults to this if not defined
    " @SpriteMoveDown/SpriteMoveLeft should be self explanatory
    """
    def __init__(self, spriteStill, position, spriteMoveUp=None, spriteMoveRight=None, spriteMoveDown=None, spriteMoveLeft=None):
        pass
    
    def Interact(self, entity):
        pass
    
    """
    " Tells an entity to move one space toward the given direction
    " Can be 0, 1, 2, 3 or can be "up", "right", "down", "left"
    """
    def Move(self, direction):
        pass

    
