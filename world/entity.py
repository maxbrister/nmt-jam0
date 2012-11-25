import numpy

"""
" The entity class should be used for anything that has a sprite, position, and can interact with other entities.
" Entities have the movement methods StartMovement, IsMoving, and Move. For immobile entities (such as a flower pot), use the ImmobileEntity class.
" The interact method is an abstract method, meant to be implemented more in later classes.
"""

class Entity:
    """
    " @SpriteStill the basic sprite, if no other sprites are defined this one is used
    " @Position a numpy.array
    " @gameBoard the gameboard object
    " @SpriteMoveUp the sprite used when the entity moves up
    "     The other movement sprites default to this if not defined (and SpriteMoveRight is not defined)
    " @SpriteMoveRight the sprite used when the entity moves right
    "     SpriteMoveLeft defaults to this if not defined
    " @SpriteMoveDown/SpriteMoveLeft should be self explanatory
    """
    def __init__(self, spriteStill, position, gameBoard, spriteMoveUp=None, spriteMoveRight=None, spriteMoveDown=None, spriteMoveLeft=None):
        self._SetSprites(spriteStill, spriteMoveUp, spriteMoveRight, spriteMoveDown, spriteMoveLeft)
        self._currentSprite = spriteStill
        self._position = numpy.array(position)
        self._oldPosition = self._position.copy()
        self._movingState = "notMoving" # a string ("notMoving", "starting", "movingOut", "movingIn" "finishing")
        self._movingFrame = 0 # an integer, starting with 0 for before the first moving query from the game loop
        self._gameBoard = gameBoard
    
    def Interact(self, entity):
        pass
    
    """
    " Tells an entity to move one space toward the given direction
    " Can be 0, 1, 2, 3 or can be "up", "right", "down", "left"
    """
    def StartMovement(self, direction):
        print "started"
        d = self.TranslateDirection(direction)
        if (direction == 0):
            self._currentSprite = self._spriteMoveUp
        if (direction == 1):
            self._currentSprite = self._spriteMoveRight
        if (direction == 2):
            self._currentSprite = self._spriteMoveDown
        if (direction == 3):
            self._currentSprite = self._spriteMoveLeft
        self._movingFrame = 0
        self._movingState = "starting"
        self._movingDirection = d

    """
    " Used by the game loop to determine if the entity is moving or not
    """
    def IsMoving(self):
        if (self._movingState == "notMoving" or self._movingState == "finishing"):
            return False
        return True

    """
    " Returns the sprite to draw, the frame of that sprite indexed at 0, and the position to draw it at as a dictionary
    "     {sprite: sprite, sprite_index: val, position: {x: val, y: val}}
    " @framesToMove the number of frames it should take to finish the animated movement
    """
    def Move(self, framesToMove):
        if (self._movingState == "finishing"):
            self._movingState = "notMoving"
        movementDirectionToDeltaPosition = numpy.array([(0,-1), (1,0), (0,1), (-1,0)])
            
        # update the state and frame
        self._movingFrame += 1
        percentDone = float(self._movingFrame)/framesToMove
        if (percentDone >= 0.5 and (self._movingState == "movingOut" or self._movingState == "starting")):
            self._movingState = "movingIn"
            self._oldPosition = self._position.copy()
            destination = self._position + movementDirectionToDeltaPosition[self._movingDirection]
            if (tuple(destination) in self._gameBoard.Movable(self._position)):
                # check that the destination is clear
                self._position += movementDirectionToDeltaPosition[self._movingDirection]
            self._gameBoard.Move(self, self._oldPosition, self._position)
        if (self._movingFrame >= framesToMove):
            self._movingState = "finishing"

        # get the position as a float value (for drawing)
        source = numpy.array(self._position, dtype=numpy.double)
        dest = source.copy()
        if (self._movingState == "movingOut" or self._movingState == "starting"):
            # moving out of the current space (happens before the middle frame)
            dest += movementDirectionToDeltaPosition[self._movingDirection]
        elif (self._movingState == "movingIn"):
            # moving into the next space (happens after the middle frame
            if (self._oldPosition != self._position).all:
                source -= movementDirectionToDeltaPosition[self._movingDirection]
            else:
                dest += movementDirectionToDeltaPosition[self._movingDirection]
        returnpos = numpy.array(self._position, dtype=numpy.double)
        if (percentDone != 0.0):
            returnpos = source+(dest-source)*percentDone
        
        return {"sprite": self._currentSprite, "sprite_index": self._movingFrame, "position": returnpos}

    """
    " translate a direction string into an integer
    " Returns 0-3 for up, right, down, left
    " Returns -1 if none of the others are found
    """
    def TranslateDirection(self, direction):
        direction = direction.lower()
        if (direction == "up" or direction == 0):
            return 0
        if (direction == "right" or direction == 1):
            return 1
        if (direction == "down" or direction == 2):
            return 2
        if (direction == "left" or direction == 3):
            return 3
        return -1

    """
    " Use this to add a new sprite to the entity after the initialization
    " @direction 0-3, or up, right, left, or down
    " @sprite the new sprite to add
    """
    def AddSprite(self, direction, sprite):
        d = self.TranslateDirection(direction);
        if (d == 0): # up
            return _SetSprites(self, self._spriteStill, sprite, self._spriteMoveRight, self._spriteMoveDown, self._spriteMoveLeft)
        if (d == 1): # right
            return _SetSprites(self, self._spriteStill, self._spriteMoveUp, sprite, self._spriteMoveDown, self._spriteMoveLeft)
        if (d == 2): # down
            return _SetSprites(self, self._spriteStill, self._spriteMoveUp, self._spriteMoveRight, sprite, self._spriteMoveLeft)
        if (d == 3): # left
            return _SetSprites(self, self._spriteStill, self._spriteMoveUp, self._spriteMoveRight, self._spriteMoveDown, sprite)

    def _SetSprites(self, still, up, right, down, left):
        self._spriteStill = still
        self._spriteMoveUp = still
        self._spriteMoveRight = still
        self._spriteMoveDown = still
        self._spriteMoveLeft = still
        if (up):
            self._spriteMoveUp = up
        if (up):
            self._spriteMoveDown = up
        if (down):
            self._spriteMoveDown = down
        if (right):
            self._spriteMoveRight = right
        if (right):
            self._spriteMoveLeft = right
        if (left):
            self._spriteMoveLeft = left

    """
    " Returns the moving state, the possibilities are listed at the attribute declaration at the top of this file
    """
    def GetMovingState(self):
        return self._movingState

if (__name__ == "__main__"):
    class Entity_GameBoardTest:
        def __init__(self):
            pass
        def Movable(self, pos):
            print pos
            x, y = pos
            return set()
            return set([(x,y), (x-1,y), (x+1,y), (x,y-1), (x,y+1)])
        def Move(self, entity, oldPosition, newPosition):
            pass

    import time
    g = Entity_GameBoardTest()
    e = Entity("spritestuff", (0, 0), g)
    while (True):
        if not (e.IsMoving()):
            e.StartMovement("right")
        print e.Move(10)
        print e.GetMovingState()
        time.sleep(0.10)
