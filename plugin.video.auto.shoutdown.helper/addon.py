import xbmc
import xbmcgui

number = xbmcgui.Dialog().numeric(0,"How many items will you watch?","2")
if number != '':
    xbmc.executebuiltin('StopScript(plugin.video.auto.shutdown)')
    xbmc.executebuiltin('RunScript(plugin.video.auto.shutdown,'+number+')')