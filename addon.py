import xbmcgui
import xbmc

#xbmc.executebuiltin("ShutDown")

class MyPlayer(xbmc.Player):
    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self)
        self.myplaycount = 0
        self.mylastplay = 0
        self.myshutdownenabled = False
        self.mylockstate = False
    
    def onPlayBackEnded(self):
        self.onPlayBackStopped()
    
    def onPlayBackStopped(self):
        print "playback stopped"
        myUnlock()
    
    def myLock(self):
        self.mylockstate = True
    
    def myUnlock(self):
        self.mylockstate = False
    
    def getLockState(self):
        return self.mylockstate

        
count = 0

heading = "How many items will you watch?"

number = xbmcgui.Dialog().numeric(0,heading)

Player = MyPlayer()

Player.myLock()

debug1 = "inserted number: "+number+", count: "+str(count)+", is playing: "+str(Player.isPlaying())+", lock state:"+str(Player.getLockState())

xbmcgui.Dialog().ok("DEBUG", debug1)
