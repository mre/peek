import wx
from PIL import Image

class Grabber():
    def __init__(self, wxApp = None):
        self.wx = wx
        self.app = wxApp

    def grab(self, pos=None, rect=100):
        if not self.app:
            self.app = self.wx.App()
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.EmptyBitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        del mem
        myWxImage = wx.ImageFromBitmap(bmp)
        im = Image.new('RGB', (myWxImage.GetWidth(), myWxImage.GetHeight()))
        im.fromstring(myWxImage.GetData())
        if pos:
            x, y = pos
            # Check bounds
            x0 = max(x-rect, 0)
            y0 = max(y-rect, 0)
            x1 = min(x+rect, size[0])
            y1 = min(y+rect, size[1])
            im = im.crop((x0,y0,x1,y1))
        return im

class Mouse():
    def __init__(self, wxApp = None):
        self.wx = wx
        self.app = wxApp

    def pos(self):
        return self.wx.GetMousePosition()

app = wx.App()

grabber = Grabber(app)
mouse = Mouse(app)

while True:
    im = grabber.grab(mouse.pos())
    im.show()
    print "pic"

"""
ff=wx.App()


#while True:
print x0, y0, x1, y1


bmp = wx.EmptyBitmap(width, height)
mem = wx.MemoryDC(bmp)
#mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
screen = wx.ScreenDC()
mem.Blit(0, 0, width, height, screen, x0, y0)
del mem
bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)
exit()
#im = bmp.ConvertToImage()
"""
