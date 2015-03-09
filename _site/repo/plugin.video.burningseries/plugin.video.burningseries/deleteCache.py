import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import sys, os

_addon_  = xbmcaddon.Addon(id='plugin.video.burningseries')
cacheFile = _addon_.getAddonInfo('path')+"/cache.data"
print "[bs][deleteCache.py] fileLocation:"+cacheFile

f = xbmcvfs.File(cacheFile, 'w')
result = f.write("")
f.close()

print "[bs][deleteCache.py] Picture Cache deleted."
