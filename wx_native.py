# show a jpeg (.jpg) image using wxPython, newer coding style
# two different ways to load and display are given
# tested with Python24 and wxPython25 vegaseat 24jul2005
 
#import cStringIO
import random
import wx

def ScreenCapture( captureStartPos, captureBmapSize, debug=False ):
    """
    General Desktop screen portion capture - partial or entire Desktop.

    My particular screen hardware configuration:
        wx.Display( 0 ) refers to the primary  Desktop display monitor screen.
        wx.Display( 1 ) refers to the extended Desktop display monitor screen (above the primary screen).

    Any particular Desktop screen size is :
        screenRect = wx.Display( n ).GetGeometry()

    Different wx.Display's in a single system may have different dimensions.
    """

    # A wx.ScreenDC provides access to the entire Desktop.
    # This includes any extended Desktop monitor screens that are enabled in the OS.
    scrDC = wx.ScreenDC()         # MSW HAS BUG:  DOES NOT INCLUDE ANY EXTENDED SCREENS.
    scrDcSize = scrDC.Size
    scrDcSizeX, scrDcSizeY = scrDcSize

    # Cross-platform adaptations :
    scrDcBmap     = scrDC.GetAsBitmap()
    scrDcBmapSize = scrDcBmap.GetSize()
    if debug :
        print 'DEBUG:  Size of scrDC.GetAsBitmap() ', scrDcBmapSize

    # Check if scrDC.GetAsBitmap() method has been implemented on this platform.
    if   not scrDcBmap.IsOk() :      # Not implemented :  Get the screen bitmap the long way.

        if debug :
            print 'DEBUG:  Using memDC.Blit() since scrDC.GetAsBitmap() is nonfunctional.'

        # Create a new empty (black) destination bitmap the size of the scrDC.
        scrDcBmap = wx.EmptyBitmap( *scrDcSize )    # Overwrire the invalid original assignment.
        scrDcBmapSizeX, scrDcBmapSizeY = scrDcSize

        # Create a DC tool that is associated with scrDcBmap.
        memDC = wx.MemoryDC( scrDcBmap )

        # Copy (blit, "Block Level Transfer") a portion of the screen bitmap
        #   into the returned capture bitmap.
        # The bitmap associated with memDC (scrDcBmap) is the blit destination.

        memDC.Blit( 0, 0,                           # Copy to this start coordinate.
                    scrDcBmapSizeX, scrDcBmapSizeY, # Copy an area this size.
                    scrDC,                          # Copy from this DC's bitmap.
                    0, 0,                    )      # Copy from this start coordinate.

        memDC.SelectObject( wx.NullBitmap )     # Finish using this wx.MemoryDC.
                                                # Release scrDcBmap for other uses.
    else :

        if debug :
            print 'DEBUG:  Using scrDC.GetAsBitmap()'

        # This platform has scrDC.GetAsBitmap() implemented.
        scrDcBmap = scrDC.GetAsBitmap()     # So easy !  Copy the entire Desktop bitmap.

        if debug :
            print 'DEBUG:  scrDcBmap.GetSize() ', scrDcBmap.GetSize()

    #end if

    return scrDcBmap.GetSubBitmap( wx.RectPS( captureStartPos, captureBmapSize ) )



class Panel1(wx.Panel):
    """ class Panel1 creates a panel with an image on it, inherits wx.Panel """
    def __init__(self, parent):
      # create the panel
      wx.Panel.__init__(self, parent, wx.ID_ANY, style=wx.SIMPLE_BORDER)
      self.Bind( wx.EVT_MOTION, self.OnMouseMotion )
      #self.Bind(wx.EVT_MOTION, self.OnMotion)
      #self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnMouseMotion(self, event):
        x = random.randint(1,500)
        y = random.randint(1,500)
        screenshot = ScreenCapture( (x,y), (x+200,y+200), debug=False )
        wx.StaticBitmap(self, -1, screenshot, (10, 5), (screenshot.GetWidth(), screenshot.GetHeight()))
        #wx.StaticBitmap(self, -1, bmp, (5, 5))
        #wx.StaticBitmap(self, -1, jpg1, (10 + jpg1.GetWidth(), 5), (jpg1.GetWidth(), jpg1.GetHeight()))

app = wx.App(False)
# create a window/frame, no parent, -1 is default ID
# increase the size of the frame for larger images
frame1 = wx.Frame(None, -1, "An image on a panel", size = (400, 300))
# call the derived class
Panel1(frame1)
frame1.Show(1)
app.MainLoop()

#app = wx.App()
