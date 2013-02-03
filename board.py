from graphics import Sprite
import numpy
import os.path

class MapError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class Tile(object):
    def __init__(self, tileName, movable):
        self.sprite = Sprite(tileName)
        self.entity = None
        self.movable = movable

    def Render(self, ctx):
        self.sprite.Render(ctx)
    
class Board(object):
    def __init__(self, mapName):
        theMap = self._MapImport(mapName)
        self._tiles = [[Tile(name, movable) for name, movable in column]
                       for column in theMap]
        
        x = 0
        y = 0
        for column in self._tiles:
            for tile in column:
                tile.sprite.position = x, y
                x += tile.sprite.width
            x = 0
            y += column[0].sprite.height

        sprite = self.GetTile((0, 0)).sprite
        self.tileWidth = sprite.width
        self.tileHeight = sprite.height
        self.tileSize = numpy.array([self.tileWidth, self.tileHeight])

    def Add(self, entity, position):
        assert self.GetEntity(position) is None
        self.GetTile(position).entity = entity

    def GetEntity(self, pos):
        return self.GetTile(pos).entity

    def GetTile(self, pos):
        return self._tiles[pos[1]][pos[0]]

    def InRange(self, pos):
        return (pos[0] >= 0 and pos[0] < len(self._tiles[0]) and
                pos[1] >= 0 and pos[1] < len(self._tiles))

    def Movable(self, position):
        ret = set()
        for pos in [(position[0]-1, position[1]),
                    (position[0]+1, position[1]),
                    (position[0]  , position[1]+1),
                    (position[0]  , position[1]-1)]:
            if (self.InRange(pos) and self.GetEntity(pos) is None
                and self.GetTile(pos).movable):
                ret.add(pos)
        
        return ret

    def Move(self, entity, oldPosition, newPosition):
        self.Remove(entity, oldPosition)
        self.Add(entity, newPosition)
            

    def Remove(self, entity, position):
        assert self.GetEntity(position) == entity
        self.GetTile(position).entity = None

    def Render(self, ctx):
        for column in self._tiles:
            for tile in column:
                tile.Render(ctx)

    def _MapImport(self, fname):
        #Read the file to a string                           
        try:                                                 
            f = open(os.path.join('maps', fname + '.mp'))    
            string = f.read()                                
        except:                                              
            raise MapError('No such file name')              
        #Separate the header and body of the map             
        array = string.split('\n')                          
        #handle null string case                             
        if array == None:                                    
            raise MapError('No map')                         
        header = array[0:1]                                  
        if header == None:                                   
            raise MapError('Invalid map')                    
        body = array[1:len(array)]                           
            #parse the header                                
        header = header[0]                                   
        references = header.split(',')                       
        ref2 = []                                            
        for reference in references:
            if '-' in reference:
                ref2.append(reference.split('-') + [True])
            elif '*' in reference:
                ref2.append(reference.split('*') + [False])
        key = {}                                             
        #create a dictionary of symbols, image names         
        for ref in ref2:                                     
            key[ref[0]] = ref[1:]
        lines = body                                         
        columns = []                                         
        for line in lines:                                   
            row = []                                         
            characters = list(line)                          
            for character in characters:                     
                row.append(key[character])                   
            columns.append(row)                              
            	                                         
        return columns[0:len(columns)-1]

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
    
