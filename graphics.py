import cairo
import numpy
import os
import os.path
import re
import pango
import pangocairo
from random import randint

CAFFEINE = False

class SpriteError(Exception):
    def __init__(self, msg, name):
        self.msg = msg + ': ' + name
    def __str__(self):
        return self.msg

class SpriteRep(object):
    DIRECTORY = 'sprites'
    FNAME_RE = re.compile(r'\A(?P<name>\w+)(-(?P<key>\w+))?\.(?P<ext>png)\Z')
    def __init__(self, name):
        name = name.lower()
        self._images = dict()
        files = os.listdir(SpriteRep.DIRECTORY)
        found = False
        for f in files:
            match = re.match(SpriteRep.FNAME_RE, f)
            if match and match.group('name').lower() == name:
                self._Load(f, match)
                
        if len(self._images) <= 0:
            raise SpriteError('File not found', name)

        for image in self._images.values():
            if image.get_width() != self.width or image.get_height() != self.height:
                raise SpriteError('Inconsitent size between subsprites', name)

        try:
            self._default = self._images['']
        except KeyError:
            self._default = self._images.values()[0]

    def Render(self, ctx, position, name):
        image = None
        name = name.lower()
        if name in self._images:
            image = self._images[name]
        else:
            image = self._default
        ctx.set_source_surface(image, position[0], position[1])
        ctx.paint()
        
    def _Load(self, fname, match):
        image = cairo.ImageSurface.create_from_png(os.path.join(SpriteRep.DIRECTORY, fname))
        key = match.group('key')
        if key is None:
            key = ''
        else:
            key = key.lower()

        self._images[key] = image
        self.width = image.get_width()
        self.height = image.get_height()

class Sprite(object):
    _repCache = dict()
    def __init__(self, name, position = (0,0)):
        self.position = position
        self.SetFrame()
        self.name = name
        self._LoadRep(name)
            
    def Render(self, ctx):
        self._rep.Render(ctx, self.position, self.animation)

    def SetFrame(self, animation = '', frame = 0):
        self.animation = animation
        self.frame = frame

    @property
    def width(self):
        return self._rep.width

    @property
    def height(self):
        return self._rep.height

    def _LoadRep(self, repName):
        if repName in Sprite._repCache:
            self._rep = Sprite._repCache[repName]
        else:
            try:
                self._rep = SpriteRep(repName)
                Sprite._repCache[repName] = self._rep
            except SpriteError as e:
                print 'SpriteError', str(e)
                if repName != 'beer':
                    self._LoadRep('beer')
                    Sprite._repCache[self.name] = self._rep
                    

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
    global CAFFEINE
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
    elif boxSize[1] is None:
        _, height = layout.get_size()
        boxSize = boxSize[0], height / pango.SCALE

    if(ALIGN_LOW):
        ctx.translate(0, boxSize[1] - (layout.get_size()[1]/pango.SCALE))

    
    if(DRAW_BACKGROUND):
        if(CAFFEINE):
            ctx.set_source_rgba(.5, .5, 0, 0.9)
            ctx.rectangle(randint(-3,3), randint(-3,3), boxSize[0] + randint(-5,5), boxSize[1] + randint(-5,5))
        else:
            ctx.set_source_rgba(0, 0, 0, 0.9)
            ctx.rectangle(0,0,boxSize[0], boxSize[1])
        ctx.fill();
        
    ctx.set_source_rgb(1, 1, 1)
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
