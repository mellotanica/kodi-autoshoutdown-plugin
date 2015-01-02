import xbmcgui
import xbmc

#xbmc.executebuiltin("ShutDown")

class MyPlayer(xbmc.Player):
    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self)
        self.old_player = kwargs['player']
        self.myplaycount = 0
        self.firstStart = True
        self.mylastplay = 0
        self.myshutdownenabled = False
        if not self.old_player.isPlaying():
            xbmcgui.Dialog().ok("Warning", "Playback must be active..")
            del self
        else:
            if self.old_player.isPlayingAudio():
                self.old_tag = self.old_player.getMusicInfoTag()
                self.newinfos = xbmcgui.ListItem(self.old_tag.getTitle())
                self.newinfos.setInfo('audio', {'title' : self.old_tag.getTitle(), 'genre' : self.old_tag.getGenre() , 'artist' : self.old_tag.getArtist() , 'album' : self.old_tag.getAlbum(), 'tracknumber' : self.old_tag.getTrack(), 'duration' : self.old_tag.getDuration(), 'year' : self.old_tag.getLyrics(), 'playcount' : self.old_tag.getPlayCount(), 'lastplayed' : self.old_tag.getLastPlayed() })
            else:
                self.old_tag = self.old_player.getVideoInfoTag()
                self.newinfos = xbmcgui.ListItem(self.old_tag.getTitle())
                self.newinfos.setInfo('video', {'title' : self.old_tag.getTitle(), 'genre' : self.old_tag.getGenre()})
            self.startpos = self.old_player.getTime()
            self.old_item = self.old_player.getPlayingFile()
            self.old_player.stop()
            self.play(self.old_item, self.newinfos, False)

    def onPlayBackStarted(self):
        if self.firstStart:
            self.seekTime(self.startpos)
            self.firstStart = false
        xbmc.Player.onPlayBackStarted(self)
        
    def onPlayBackEnded(self):
        self.onPlayBackStopped()
    
    def onPlayBackStopped(self):
        self.myplaycount = self.myplaycount+1

        
count = 0

heading = "How many items will you watch?"

number = xbmcgui.Dialog().numeric(0,heading)

old_player = xbmc.Player()

Player = MyPlayer(player=old_player)

debug1 = "inserted number: "+number+", count: "+str(count)+", is playing: "+str(Player.isPlaying())+" old playing: "+str(old_player.isPlaying())

#xbmcgui.Dialog().ok("DEBUG", debug1)

test = True

while test:
    xbmcgui.Dialog().notification("DEBUG", "still waiting..", time=1000)
    xbmc.sleep(7000)
    try:
        test = Player.isPlaying()
    except:
        test = False

xbmcgui.Dialog().notification("DEBUG", "script terminated.", time=2000)