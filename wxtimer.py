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

class Frame(wx.Frame):
     def __init__(self):
         wx.Frame.__init__(self, None, size=(300, 300))
         self.timer = wx.Timer(self)
         self.Bind(wx.EVT_TIMER, self.update_title)
         self.timer.Start(3000)  # in miliseconds

     def update_title(self, event):
        pos = wx.GetMousePosition()
        print pos
        screenshot = ScreenCapture( (pos.x,pos.y), (pos.x+200,pos.y+200), debug=False )
        wx.StaticBitmap(self, -1, screenshot, (10, 5), (screenshot.GetWidth(), screenshot.GetHeight()))
        #screenshot.SetOption(wx.PngZL, 7)
        scr = screenshot.ConvertToImage()
        scr.SetOption(wx.IMAGE_OPTION_PNG_COMPRESSION_LEVEL, 7)
        scr.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)

app = wx.App(redirect=False)
top = Frame()
top.Show()
app.MainLoop()
