import entity
import graphics
import maps.tileset
import numpy
import os.path
import re

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

    ENTITY_KEY_RES = (re.compile(r'(?P<entity>(?P<sprite>\w+))$'),
                      re.compile(r'(?P<entity>(?P<sprite>\w+)\d+)$'),
                      re.compile(r'(?P<entity>[\w\s]+)-(?P<sprite>\w+)$'))
    CREATURE_RE = re.compile(r'(?P<name>\w+)(?P<level>\d+)$')
    def _FinishLoad(self):
        sprite = self.GetTile((0, 0)).sprite
        self.tileWidth = sprite.width
        self.tileHeight = sprite.height
        self.tileSize = numpy.array([self.tileWidth, self.tileHeight])
        for y in xrange(len(self._tiles)):
            for x in xrange(len(self._tiles[0])):
                self._PlaceTile((x, y))

        self._entities = set()

        # load the entities table
        battleframe = __import__('battleframe')
        creature = __import__('creature')
        mod = __import__('maps.{0}'.format(self.name))
        mod = getattr(mod, self.name)
        entityTable = mod.entities
        containerList = mod.containers
        entities = dict()
        for name, info in entityTable.items():
            # The name may be
            # a) sprite_name
            # b) sprite_name<num>
            # c) entity_name-sprite_name
            spriteName = entityName = None
            for are in Board.ENTITY_KEY_RES:
                match = re.match(are, name)
                if match:
                    spriteName = match.group('sprite')
                    entityName = match.group('entity')
            if entityName is None or spriteName is None:
                raise MapError('Unable to parse entity key: "{0}"'.format(name))

            #        0                      1                  2
            # info: [list-of-conversations, list-of-creatures, position]
            ent = entity.NPC(entityName, spriteName, info[2], self)
            entities[entityName] = ent
            for conversation in info[0]:
                # The conversaion may end in `~plot_event or `~BATTLE
                # these indicate plot completion event, or battle start
                finishEvent = lambda player, npc: None
                if len(conversation[-1]) >= 2 and conversation[-1][:2] == '`~':
                    if conversation[-1] == '`~BATTLE':
                        finishEvent = lambda player, npc: battleframe.StartFight(player, npc)
                    else:
                        event = conversation[-1][2:]
                        finishEvent = lambda player, npc, event=event: player.FinishPlotEvent(event)
                    conversation = conversation[:-1]
                ent.AddToDialogueList(conversation[0], conversation[1:], finishEvent)

            for cdesc in info[1]:
                match = re.match(Board.CREATURE_RE, cdesc)
                if not match:
                    raise MapError('Unable to parse creature "{0}" for key "{1}"'.format(cdesc, name))
                # TODO level up
                c = creature.Creature(match.group('name'))
                ent.AddCreature(c)

        containers = list()
        for spriteName, pos in containerList:
            container = entity.Container(spriteName, pos, self)
            containers.append(container)
        
        # initialize the entities
        mod = __import__('maps.{0}_init'.format(self.name))
        initFn = getattr(mod, '{0}_init'.format(self.name)).Initialize
        initFn(__import__('menuframe'), battleframe, creature, entity, self, entities, containers)

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
    
