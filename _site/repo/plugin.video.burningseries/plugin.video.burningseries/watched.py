import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs

addonInfo = xbmcaddon.Addon()
watchedFile = addonInfo.getAddonInfo('path')+"/watched.data"

# since 1.3.0
def writeWatchedData(url):
	global watchedFile
	f = xbmcvfs.File(watchedFile)
	d = f.read()
	f.close()
	f = xbmcvfs.File(watchedFile, 'w')
	b = d+url+"\n"
	result = f.write(b)
	print "[bs][writeWatchedData] write "+watchedFile+" -> "+ url
	f.close()
	return result
	
def readWatchedData(url):
	global watchedFile
	f = xbmcvfs.File(watchedFile)
	b = f.read()
	f.close()
	watchedData = b.splitlines()
	for n in watchedData:
		if url == n:
			print "[bs][readWatchedData] found "+url+" in watched.data"
			return True
	print "[bs][readWatchedData] "+url+" not found in watched.data"
	return False

def changeToWatched(watchedString):
	# -- rewrite listentry
	return "[I]"+watchedString+"[/I]" + " watched"

def markParentEntry(urlData):
	if not readWatchedData(urlData):
		writeWatchedData(urlData)
