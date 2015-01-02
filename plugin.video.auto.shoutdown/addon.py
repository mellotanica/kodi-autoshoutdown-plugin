import xbmcgui
import xbmc
import sys

debugActive = False

noMoreFilesTimeout = 10

def countToZero(start):
    s = start
    while s > 0:
        infoNot(str(s)+"..",1000)
        xbmc.sleep(1000)
        if xbmc.abortRequested:
            return True
        s = s - 1
    return False

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
        self.mylastplay = int(kwargs['items'])
        self.mytimeout = int(kwargs['timeout'])
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
        debNot("file ended, count: "+str(self.myplaycount)+" total: "+str(self.mylastplay))
        if self.myplaycount >= self.mylastplay:
            self.terminatedExecution = True
            infoNot("All desired items played, will shout down in 3 seconds..")
            xbmc.sleep(3000)
            if xbmc.abortRequested:
                    return
            xbmc.executebuiltin('ShutDown()')
        else:
            if self.old_item < len(self.myplaylist):
                debNot("will now play "+str(self.myplaylist[self.old_item].getfilename()))
                self.play(self.myplaylist, startpos=self.old_item)
            else:
                self.terminatedExecution = True
                infoNot("Playlist is empty, will shout down in "+str(self.mytimeout)+" seconds...", 5000, playsound=True)
                if self.mytimeout >= 5:
                    xbmc.sleep(5000)
                    if xbmc.abortRequested:
                        return
                    self.mytimeout = self.mytimeout - 5
                    if countToZero(self.mytimeout):
                        return
                    xbmc.executebuiltin('ShutDown()')
                else:
                    xbmc.sleep(self.mytimeout*1000)
                    if xbmc.abortRequested:
                        return
                    xbmc.executebuiltin('ShutDown()')
    
    def getClearToGo(self):
        return self.terminatedExecution

Player = MyPlayer(player=xbmc.Player(), items=int(sys.argv[1]), timeout=noMoreFilesTimeout)

test = not Player.getClearToGo()
if test:
    infoNot("will reproduce "+sys.argv[1]+" elements from playlist and shout down", 3000)

cycle = 0

while test:
    if xbmc.abortRequested:
        break
    xbmc.sleep(500)
    if cycle < 8:
        cycle = cycle+1
        continue
    else:
        cycle = 0
    try:
        test = not Player.getClearToGo()
    except:
        test = False

debNot("script terminated.")
