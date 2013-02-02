from graphics import Sprite
import mapparser

class Tile(object):
    def __init__(self, tileName):
        self.sprite = Sprite(tileName)

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

    def Render(self, ctx):
        for column in self._tiles:
            for tile in column:
                tile.Render(ctx)

    def Movable(position):
        ret = set()
        return ret

if __name__ == '__main__':
    import main
    board = Board('test')
    def RenderBoard(ctx, size):
        board.Render(ctx)
        return True
    win = main.Window('Board Test')
    win.run(RenderBoard)
    
