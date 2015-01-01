import xbmcaddon
import xbmcgui

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

line1 = "first try"

xbmcgui.Dialog().ok(addonname, line1)