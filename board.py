import entity
import graphics
import maps.tileset
import numpy
import os.path

from graphics import Sprite

class MapError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class Tile(object):
    def __init__(self, tileName, sprite, movable):
        self.name = tileName
        self.sprite = Sprite(sprite)
        self.entity = None
        self.movable = movable

    def Render(self, ctx):
        self.sprite.Render(ctx)
    
class Board(object):
    def __init__(self, mapName):
        # create the board
        self.name = mapName

        self._Load(mapName)

    @property
    def entities(self):
        return list(self._entities)

    def Add(self, entity, position):
        assert self.GetEntity(position) is None
        self.GetTile(position).entity = entity
        self._entities.add(entity)

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
        self._entities.remove(entity)

    def Render(self, ctx):
        for column in self._tiles:
            for tile in column:
                tile.Render(ctx)

        for ent in self.entities:
            ent.Render(ctx)

    def SaveTiles(self, mapName = None):
        '''
        Save the tile state, but not the contained entities.

        fname - Name of the map, defaults to self.name
        '''
        mapName = mapName or self.name
        try:
            with open(self._FileForName(mapName), 'wb') as fout:
                for line in self._tiles:
                    for idx, tile in enumerate(line):
                        fout.write(tile.name)
                        if idx+1 < len(line):
                            fout.write(',')
                    fout.write('\n')
        except IOError:
            raise MapError('Save failed')

    def _FileForName(self, name):
        return os.path.join('maps', name + '.mp')


    def _Load(self, name):
        try:
            with open(self._FileForName(name)) as fin:
                lines = fin.readlines()
        except IOError:
            raise MapError('Map load failed: ' + name)
        
        self._tiles = [[self._LoadTile(tname) for tname in line.split(',')] for line in lines]

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

        self._entities = set()

        # load the entities
        mod = __import__('maps.' + name)
        getattr(mod, 'test').Initialize(__import__('menuframe'), __import__('battleframe'), __import__('creature'), entity, self)

    def _LoadTile(self, tname):            
        tiles = maps.tileset.tiles
        tname = tname.strip()
        while tname[-1] in ['\n', '\r']:
            tname = tname[:-1]
        tileInfo = tiles[tname.strip()]

        def GetInfo(tileInfo, key, default):
            if tileInfo is None or key not in tileInfo:
                return default
            return tileInfo[key]
        getInfo = lambda key, default, tileInfo=tileInfo: GetInfo(tileInfo, key, default)
        
        sprite = getInfo('bottom', tname)
        movable = getInfo('movable', True)
        top = getInfo('top', None)
        spawn = getInfo('spawn', [])

        # TODO: Use the rest of the parameters
        return Tile(tname, sprite, movable)

if __name__ == '__main__':
    import main
    board = Board('test')
    board.SaveTiles()
    
