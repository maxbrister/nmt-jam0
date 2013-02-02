import cairo
import Image
import numpy
import os
import os.path
import re

_cairoFormats = {3: cairo.FORMAT_RGB24, 4: cairo.FORMAT_ARGB32}
def PILToCairo(im):
    im.putalpha(256)
    arr = numpy.array(im)
    height, width, channels = arr.shape
    fmt = _cairoFormats[channels]
    surface = cairo.ImageSurface.create_for_data(arr, fmt,
                                                 width, height)
    return surface

class SpriteError(Exception):
    def __init__(self, msg, name):
        self.msg = msg + ': ' + name
    def __str__(self):
        return self.msg

class SpriteRep(object):
    DIRECTORY = 'sprites'
    def __init__(self, name):
        files = os.listdir(SpriteRep.DIRECTORY)
        found = False
        for f in files:
            if len(f) > len(name) and f[:len(name)] == name:
                self._load(f)
                found = True
                break
        if not found:
            raise SpriteError('File not found', name)

    def render(self, ctx, position):
        ctx.set_source_surface(self.image, position[0], position[1])
        ctx.paint()
        
    def _load(self, fname):
        # file name format: name_widthxheight.ext
        img = Image.open(os.path.join(SpriteRep.DIRECTORY, fname))
        self.image = PILToCairo(img)
        match = re.match(r'\A\w+-(?P<width>\d+)x(?P<height>\d+)\.\w+\Z', fname)
        if match:
            # animated sprite
            self.width = int(match.group('width'))
            self.height = int(match.group('height'))
            self.frames = self.width / img.size[0]
        else:
            self.width, self.height = img.size
            self.frames = 1

allReps = dict()

class Sprite(object):
    def __init__(self, name, position = (0,0)):
        self.position = position
        if name in allReps:
            self._rep = allReps[name]
        else:
            self._rep = SpriteRep(name)
            allReps[name] = self._rep
            
    def render(self, ctx):
        self._rep.render(ctx, self.position)

    @property
    def width(self):
        return self._rep.width

    @property
    def height(self):
        return self._rep.height

if __name__ == '__main__':
    import main
    testSprite = Sprite('test')
    def graphicsMain(ctx):
        testSprite.render(ctx)
        return True
    win = main.Window('Graphics test')
    win.run(graphicsMain)
