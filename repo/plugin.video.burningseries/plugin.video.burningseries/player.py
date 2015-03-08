import xbmc
from watched import *

class bsPlayer(xbmc.Player):
	def __init__( self, *args, **kwargs ):
		xbmc.Player.__init__( self )

	def playStream(self, url, bsUrl):
		self.play(url)
		done = False
		if readWatchedData(bsUrl):
			done = True
		while (not xbmc.abortRequested and self.isPlaying()):
			totalTime = self.getTotalTime()
			tRemain =  totalTime - self.getTime()
			if totalTime<60:
				relativeWatched = 5
			else:
				relativeWatched = 10
			if tRemain<(totalTime/100*relativeWatched) and not done:
				print "[bs][playStream] marked as watched :"+bsUrl
				writeWatchedData(bsUrl)
				done = True
			xbmc.sleep(1000)

	def onPlayBackStarted(self):
		print "[bs][bsPlayer] PLAYBACK STARTED"
    
	def onPlayBackEnded(self):
		print "[bs][bsPlayer] PLAYBACK ENDED"

	def onPlayBackStopped(self):
		print "[bs][bsPlayer] PLAYBACK STOPPED"