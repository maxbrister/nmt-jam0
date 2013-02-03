import cairo
import numpy
import os
import os.path
import re

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
        self.image = cairo.ImageSurface.create_from_png(os.path.join(SpriteRep.DIRECTORY, fname))
        match = re.match(r'\A\w+-(?P<width>\d+)x(?P<height>\d+)\.\w+\Z', fname)
        if match:
            # animated sprite
            self.width = int(match.group('width'))
            self.height = int(match.group('height'))
            self.frames = self.width / self.image.get_width()
        else:
            self.width = self.image.get_width()
            self.height = self.image.get_height()
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
        self._rep.Render(ctx, self.position, background)

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
    ctx.select_font_face('monospace')

    #TITLE BLOCK
    ctx.rectangle(20,40, len(title)*40 + 20, 95)
    ctx.set_source_rgba(0.1, 0.1, 0.1, 0.82) # Solid color
    ctx.fill()

    ctx.rectangle(20,40, len(title)*40 + 20, 95)
    ctx.set_source_rgb (0.5, 0.5, 0.5) # Solid color
    ctx.set_line_width(5)
    ctx.stroke()

    ctx.move_to(40, 100)
    ctx.set_font_size(50)
    ctx.text_path(title)
    ctx.set_line_width(2)
    ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
    ctx.stroke()

    #OPTIONS BLOCK
    ctx.rectangle(130,170, 350, len(options)*35 + 10)
    ctx.set_source_rgba(0.1, 0.1, 0.1, 0.82) # Solid color
    ctx.fill()

    ctx.rectangle(130,170, 350, len(options)*35 + 5)
    ctx.set_source_rgb (0.5, 0.5, 0.5) # Solid color
    ctx.set_line_width(5)
    ctx.stroke()

    ctx.set_font_size(30)
    ctx.set_line_width(2)
    element = 0

    for option in options:
        if element == selected:
            option = '>>> ' + option
        ctx.move_to(150, 200 + 30*element)
        ctx.text_path(option)
        element += 1

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
