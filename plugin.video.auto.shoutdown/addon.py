import xbmcgui
import xbmc
import sys

debugActive = True

def infoNot(text, showtime=2000, header="Info", playsound=False):
    xbmcgui.Dialog().notification(heading=header, message=text, time=showtime, sound=playsound)

def debNot(text, time=2000):
    if debugActive:
        infoNot(text, header="DEBUG", showtime=time)
        
class MyPlayer(xbmc.Player):
    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self)
        self.old_player = kwargs['player']
        self.myplaycount = 0
        self.mylastplay = kwargs['items']
        self.myshutdownenabled = False
        self.terminatedExecution = False
        if not self.old_player.isPlaying():
            self.terminatedExecution = True
            xbmcgui.Dialog().notification("Warning", "Playback must be active..", icon=xbmcgui.NOTIFICATION_WARNING, time=5000)            
        else:
            self.myplaylist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            self.old_item = self.myplaylist.getposition()
            self.play()
        
    def onPlayBackEnded(self):
        self.myplaycount = self.myplaycount+1
        self.old_item = self.old_item + 1
        if self.myplaycount >= self.mylastplay:
            self.terminatedExecution = True
            infoNot("All desired items played, will shout down in 3 seconds..")
            xbmc.sleep(3000)
            debNot("SHOUTDOWN")
            #xbmc.executebuiltin('ShutDown()')
        else:
            if self.old_item < len(self.myplaylist):
                self.play(self.myplaylist, startpos=self.old_item)
            else:
                self.terminatedExecution = True
                infoNot("Playlist is empty, will shout down in 10 seconds...", 5000, playsound=True)
                xbmc.sleep(5000)
                infoNot("5..",1000)
                xbmc.sleep(1000)
                infoNot("4..",1000)
                xbmc.sleep(1000)
                infoNot("3..",1000)
                xbmc.sleep(1000)
                infoNot("2..",1000)
                xbmc.sleep(1000)
                infoNot("1..",1000)
                xbmc.sleep(1000)
                infoNot("Bye",1000)
                debNot("SHOUTDOWN")
                #xbmc.executebuiltin('ShutDown()')
    
    def getClearToGo(self):
        return self.terminatedExecution

Player = MyPlayer(player=xbmc.Player(), items=int(sys.argv[1]))

test = not Player.getClearToGo()
if test:
    infoNot("will reproduce "+sys.argv[1]+" elements from playlist and shout down", 3000)

while test:
    xbmc.sleep(3000)
    try:
        test = not Player.getClearToGo()
    except:
        test = False

debNot("script terminated.")