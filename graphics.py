import cairo
import Image
import numpy
import os
import os.path
import re

_cairoFormats = {3: cairo.FORMAT_RGB24, 4: cairo.FORMAT_ARGB32}
def PILToCairo(im):
    im.putalpha(256) # what happens if image has alpha already?
    arr = numpy.array(im)
    height, width, channels = arr.shape

    # kludge because channels in PIL and cairo are swaped
    for r in xrange(height):
        for c in xrange(width):
            temp = arr[r][c][0]
            arr[r][c][0] = arr[r][c][2]
            arr[r][c][2] = temp
            
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
                self._Load(f)
                found = True
                break
        if not found:
            raise SpriteError('File not found', name)

    def Render(self, ctx, position):
        ctx.set_source_surface(self.image, position[0], position[1])
        ctx.paint()
        
    def _Load(self, fname):
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
            
    def Render(self, ctx):
        self._rep.Render(ctx, self.position)

    def SetFrame(self, animation = '', frame = 0):
        pass

    @property
    def width(self):
        return self._rep.width

    @property
    def height(self):
        return self._rep.height

def RenderMenu(ctx, title, options, selected):
        #ctx.translate (0.1, 0.1) # Changing the current transformation matrix
    ctx.move_to (30, 30)
    ctx.select_font_face('monospace')
    ctx.set_font_size(30)
    ctx.text_path('THIS IS SOME TEXT, YO!')
    ctx.text_path('More Text!')
    ctx.text_path('How does this work?!')
        #ctx.show_text('This is some text, yo!')
    ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
    ctx.stroke ()
    
if __name__ == '__main__':
    import main
    testSprite = Sprite('test')
    def graphicsMain(ctx, size):
        testSprite.Render(ctx)
        return True
    win = main.Window('Graphics test')
    win.run(graphicsMain)
