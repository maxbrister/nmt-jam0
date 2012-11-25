class Entity:
    __spriteStill = None
    __spriteMoveUp = None
    __spriteMoveDown = None
    __spriteMoveLeft = None
    __spriteMoveRight = None
    __position = None # a dictionary {x: val, y: val}
    __currentSprite = None
    __movingDirection = None # an integer
    __movingState = None # a string ("notMoving", "starting", "movingOut", "movingIn" "finishing")
    __movingFrame = None # an integer, starting with 0 for before the first moving query from the game loop

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
        self.__SetSprites(spriteStill, spriteMoveUp, spriteMoveRight, spriteMoveDown, spriteMoveLeft)
        self.__currentSprite = spriteStill
        self.__position = position
    
    def Interact(self, entity):
        pass
    
    """
    " Tells an entity to move one space toward the given direction
    " Can be 0, 1, 2, 3 or can be "up", "right", "down", "left"
    """
    def StartMovement(self, direction):
        d = TranslateDirection(direction)
        if (direction == 0):
            self.__currentSprite = self.__spriteMoveUp
        if (direction == 1):
            self.__currentSprite = self.__spriteMoveRight
        if (direction == 2):
            self.__currentSprite = self.__spriteMoveDown
        if (direction == 3):
            self.__currentSprite = self.__spriteMoveLeft
        self.__movingFrame = 0
        self.__movingState = "starting"
        self.__movingDirection = d

    """
    " Used by the game loop to determine if the entity is moving or not
    """
    def IsMoving(self):
        if (self.__movingState == "notMoving"):
            return False
        return True

    """
    " Returns the sprite to draw, the frame of that sprite indexed at 0, and the position to draw it at as a dictionary
    "     {sprite: sprite, sprite_index: val, position: {x: val, y: val}}
    " @gameBoard the gameboard object
    " @framesToMove the number of frames it should take to finish the animated movement
    """
    def Move(self, gameBoard, framesToMove):
        if (self.__movingState == "finishing"):
            self.__movingState = "notMoving"
            
        # update the state and frame
        self.__movingFrame += 1
        percentDone = self.__movingFrame/framesToMove
        if (percentDone >= 0.5 and (self.__movingState == "movingOut" or self.__movingState == "starting")):
            self.__movingState = "movingIn"
            x = self.__position["x"]
            y = self.__position["y"]
            if (self.__movingDirection == 0 and (x,y-1) in gameBoard.movable(x,y)):
                self.__position["y"] -= 1
            elif (self.__movingDirection == 1 and (x+1,y) in gameBoard.movable(x,y)):
                self.__position["x"] += 1
            elif (self.__movingDirection == 2 and (x,y+1) in gameBoard.movable(x,y)):
                self.__position["y"] += 1
            elif (self.__movingDirection == 3 and (x-1,y) in gameBoard.movable(x,y)):
                self.__position["x"] -= 1
        if (self.__movingFrame >= framesToMove):
            self.__movingState = "finishing"

        # get the position as a float value
        xsource = self.__position["x"]
        ysource = self.__position["y"]
        xdest = self.__position["x"]
        ydest = self.__position["y"]
        if (self.__movingState == "movingOut" or self.__movingState == "starting"):
            # moving out of the current space
            if (self.__movingDirection == 0):
                ydest -= 1
            elif (self.__movingDirection == 1):
                xdest += 1
            elif (self.__movingDirection == 2):
                ydest += 1
            elif (self.__movingDirection == 3):
                xdest -= 1
        else:
            # moving into the next space
            if (self.__movingDirection == 0):
                ysource += 1
            elif (self.__movingDirection == 1):
                xsource -= 1
            elif (self.__movingDirection == 2):
                ysource -= 1
            elif (self.__movingDirection == 3):
                xsource += 1
        returnx = xsource+(xdest-xsource)/percentDone
        returny = ysource+(ydest-ysource)/percentDone
        
        return {"sprite": self.__currentSprite, "sprite_index": self.__movingFrame, "position": {"x": returnx, "y": returny}}
    
    """
    " translate a direction string into an integer
    " Returns 0-3 for up, right, down, left
    " Returns -1 if none of the others are found
    """
    def TranslateDirection(direction):
        direction = lower(direction)
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
        d = TranslateDirection(direction);
        if (d == 0): # up
            return __SetSprites(self, self.__spriteStill, sprite, self.__spriteMoveRight, self.__spriteMoveDown, self.__spriteMoveLeft)
        if (d == 1): # right
            return __SetSprites(self, self.__spriteStill, self.__spriteMoveUp, sprite, self.__spriteMoveDown, self.__spriteMoveLeft)
        if (d == 2): # down
            return __SetSprites(self, self.__spriteStill, self.__spriteMoveUp, self.__spriteMoveRight, sprite, self.__spriteMoveLeft)
        if (d == 3): # left
            return __SetSprites(self, self.__spriteStill, self.__spriteMoveUp, self.__spriteMoveRight, self.__spriteMoveDown, sprite)

    def __SetSprites(self, still, up, right, down, left):
        self.__spriteStill = still
        self.__spriteMoveUp = still
        self.__spriteMoveRight = still
        self.__spriteMoveDown = still
        self.__spriteMoveLeft = still
        if (up):
            self.__spriteMoveUp = up
        if (up):
            self.__spriteMoveDown = up
        if (down):
            self.__spriteMoveDown = down
        if (right):
            self.__spriteMoveRight = right
        if (right):
            self.__spriteMoveLeft = right
        if (left):
            self.__spriteMoveLeft = left
