import xbmcgui
import xbmc

#xbmc.executebuiltin("ShutDown")

class MyPlayer(xbmc.Player):
    def onPlayBackEnded(self):
        xbmcgui.Dialog().ok("play ended")
    

count = 0

heading = "How many items will you watch?"

number = xbmcgui.Dialog().numeric(0,heading)

debug1 = "inserted number: "+number+", count: "+str(count)+", is playing: "+str(xbmc.Player().isPlaying())

xbmcgui.Dialog().ok("DEBUG", debug1)

xbmc.Player = MyPlayer()