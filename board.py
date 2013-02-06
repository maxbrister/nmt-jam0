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
    def __init__(self, mapName, newSize = None):
        # create the board
        self.name = mapName

        try:
            self._Load(mapName)
        except MapError:
            if newSize is None:
                raise

            self._tiles = [[self._LoadTile('blank') for r in newSize[0]] for c in newSize[1]]
        self._FinishLoad()
        if newSize is not None:
            diff = newSize[1] - len(self._tiles)
            if diff < 0:
                del self._tiles[newSize[1]:]
            elif diff > 0:
                self._tiles += [[self._LoadTile('blank') for _ in xrange(len(self._tiles[0]))]
                                for _ in xrange(diff)]

            diff = newSize[0] - len(self._tiles[0])
            if diff < 0:
                for column in self._tiles:
                    del column[newSize[0]:]
            elif diff > 0:
                for column in self._tiles:
                    column += [self._LoadTile('blank') for _ in xrange(diff)]
            
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

    def GetTileName(self, pos):
        return self._tiles[pos[1]][pos[0]].name

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

    def RenderLines(self, ctx):
        for c in xrange(len(self._tiles[0])+1):
            ctx.move_to(c * self.tileWidth, 0)
            ctx.line_to(c * self.tileWidth, len(self._tiles) * self.tileHeight)
        for r in xrange(len(self._tiles)+1):
            ctx.move_to(0, r * self.tileHeight)
            ctx.line_to(len(self._tiles[0]) * self.tileWidth, r * self.tileHeight)
        ctx.stroke()

    def ReplaceTile(self, pos, tileName):
        '''
        Replace the tile at (pos.x, pos.y) with a new tile of the given name.
        Will try to move the entity on the tile. If unable to move the entity, will return the entity.

        return - The removed entity, or None
        '''
        
        ent = self.GetEntity(pos)
        if ent is not None:
            self.Remove(ent, pos)
        self._tiles[pos[1]][pos[0]] = self._LoadTile(tileName)
        self._PlaceTile(pos)
        
        if ent is not None and self.GetTile(pos).movable:
            self.Add(ent, pos)
            return None
        return ent
        

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
        
    def _FinishLoad(self):
        sprite = self.GetTile((0, 0)).sprite
        self.tileWidth = sprite.width
        self.tileHeight = sprite.height
        self.tileSize = numpy.array([self.tileWidth, self.tileHeight])
        for y in xrange(len(self._tiles)):
            for x in xrange(len(self._tiles[0])):
                self._PlaceTile((x, y))

        self._entities = set()

        # load the entities
        mod = __import__('maps.{0}'.format(self.name))
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

    def _PlaceTile(self, pos):
        tile = self.GetTile(pos)
        tile.sprite.position = pos[0] * self.tileWidth, pos[1] * self.tileHeight

if __name__ == '__main__':
    import main
    board = Board('test')
    board.SaveTiles()
    
