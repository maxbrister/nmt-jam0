from graphics import Sprite
import mapparser

class Tile(object):
    def __init__(self, tileName):
        self.sprite = Sprite(tileName)
        self.entity = None

    def Render(self, ctx):
        self.sprite.render(ctx)
    
class Board(object):
    def __init__(self, mapName):
        theMap = mapparser.MapImport(mapName)
        self._tiles = [[Tile(t) for t in column] for column in theMap]
        
        x = 0
        y = 0
        for column in self._tiles:
            for tile in column:
                tile.sprite.position = x, y
                x += tile.sprite.width
            x = 0
            y += column[0].sprite.height

    def Add(self, entity, position):
        assert GetEntity(position) is None
        GetTile(position).entity = entity

    def GetEntity(self, pos):
        return GetTile(pos).entity

    def GetTile(self, pos):
        return self._tiles[pos[0]][pos[1]]

    def InRange(self, pos):
        return (pos[0] >= 0 and pos[0] < len(self._tiles) and
                pos[1] >= 0 and pos[1] < len(self._tiles[0]))

    def Movable(self, position):
        ret = set()
        for pos in [(position[0]-1, position[1]),
                    (position[0]+1, position[1]),
                    (position[0]  , position[1]+1),
                    (position[0]  , position[1]-1)]:
            if self.InRange(pos) and self.GetTile(pos).entity is None:
                ret.add(pos)
        
        return ret

    def Move(self, entity, oldPosition, newPosition):
        Remove(entity, oldPosition)
        Add(entity, newPosition)
            

    def Remove(self, entity, position):
        assert GetEntity(position) == entity
        GetTile(position).entity = None

    def Render(self, ctx):
        for column in self._tiles:
            for tile in column:
                tile.Render(ctx)

if __name__ == '__main__':
    import main
    board = Board('test')

    assert board.Movable((0,0)) == set([(1,0),(0,1)])
    assert board.Movable((1,1)) == set([(1,0), (1,2), (0,1), (2,1)])
    
    def RenderBoard(ctx, size):
        board.Render(ctx)
        return True
    win = main.Window('Board Test')
    win.run(RenderBoard)
    
