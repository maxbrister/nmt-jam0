import cairo
import numpy
import os
import os.path
import re
import pango
import pangocairo

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
            if len(f) > len(name) and f[:len(name)] == name and f[-3:] == 'png':
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
        self._rep.Render(ctx, self.position)

    def SetFrame(self, animation = '', frame = 0):
        pass

    @property
    def width(self):
        return self._rep.width

    @property
    def height(self):
        return self._rep.height

def _PangoFont(layout, fontSize, fontName='Sans'):
    font = pango.FontDescription(fontName + ' ' + str(fontSize))
    layout.set_font_description(font)

def RenderMenu(ctx, title, options, selected, position, fontSizeTitle, fontSize):
    ctx.save()
    ctx.translate(position[0], position[1])
    pangoCtx = pangocairo.CairoContext(ctx)

    #TITLE BLOCK
    if title is not None:
        width, height = DisplayTextBox(ctx, title, textSize=fontSizeTitle)
        ctx.translate(110, 35 + height)

    #OPTIONS BLOCK

    # find the bigest possible options block
    bigText = '\n'.join('>>> ' + option for option in options)
    size = TextBoxSize(ctx, bigText, fontSize)
    size = [s + 10 for s in size]
        
    optionsText = list()
    for index, option in enumerate(options):
        if index == selected:
            option = '>>> ' + option
        optionsText.append(option)
        
    optionsText = '\n'.join(optionsText)
    DisplayTextBox(ctx, optionsText, boxSize=size, textSize=fontSize)

    ctx.restore()

def TextBoxSize(ctx, text, fontSize=20, width=-1):
    pangoCtx = pangocairo.CairoContext(ctx)
    layout = pangoCtx.create_layout()
    _PangoFont(layout, fontSize)
    layout.set_text(text)
    layout.set_width(width)
    pangoCtx.update_layout(layout)
    width, height = layout.get_size()
    return width / pango.SCALE, height / pango.SCALE

'''
ALIGN_LOW : Aligns to the bottom of the specified box
DRAW_BACKGROUND : Draws a background behind the text
'''
def DisplayTextBox(ctx, text, location=(0,0), boxSize=None, textSize=20, ALIGN_LOW=False, DRAW_BACKGROUND=True):
    ctx.save()
    
    ctx.translate(location[0], location[1])
    
    pangocairo_ctx = pangocairo.CairoContext(ctx)
    
    layout = pangocairo_ctx.create_layout()
    _PangoFont(layout, textSize)

    if boxSize is None:
        layout.set_width(-1)
    else:
        layout.set_width(boxSize[0]*pango.SCALE)
    
    layout.set_text(text)
    
    pangocairo_ctx.update_layout(layout)

    if boxSize is None:
        width, height = layout.get_size()
        boxSize = width / pango.SCALE, height / pango.SCALE

    if(ALIGN_LOW):
        ctx.translate(0, boxSize[1] - (layout.get_size()[1]/pango.SCALE))
    
    if(DRAW_BACKGROUND):
        ctx.set_source_rgb(0.5, 0.5, 0.5)
        ctx.rectangle(0, 0, boxSize[0], boxSize[1])
        ctx.fill();
        
    ctx.set_source_rgb(1,1,1)
    pangocairo_ctx.show_layout(layout)

    ctx.restore()
    return boxSize
    
if __name__ == '__main__':
    import main
    testSprite = Sprite('test')
    def graphicsMain(ctx, size):
        testSprite.Render(ctx)
        return True
    win = main.Window('Graphics test')
    win.run(graphicsMain)
