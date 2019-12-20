import xbmc

from resources.lib import logger
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.handler.ParameterHandler import ParameterHandler


class XstreamPlayer(xbmc.Player):
    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self, *args, **kwargs)        
        self.streamFinished = False
        self.streamSuccess = True
        self.playedTime = 0
        self.totalTime = 999999
        logger.info('player instance created')
    
    def onPlayBackStarted(self):
        logger.info('starting Playback')
        self.totalTime = self.getTotalTime()

    def onPlayBackStopped(self):
        logger.info('Playback stopped')
        if self.playedTime == 0 and self.totalTime == 999999:
            self.streamSuccess = False
            logger.error('Kodi failed to open stream')

        self.streamFinished = True

        if cConfig().getSetting('metahandler') == 'true':
            from xstream import get_metahandler
            meta = get_metahandler()

            if meta:
                try:
                    percent = self.playedTime/self.totalTime
                    logger.info('Watched percent '+str(int(percent*100)))
                    if percent >= 0.80:
                        logger.info('Attemt to change watched status')
                        params = ParameterHandler()
                        season = ''
                        episode = ''
                        mediaType = params.getValue('mediaType')
                        imdbID = params.getValue('imdbID')
                        name = params.getValue('Title')
                        TVShowTitle = params.getValue('TVShowTitle')
                        if params.exist('season'):
                            season = params.getValue('season')
                            if int(season) > 0:mediaType = 'season'
                        if params.exist('episode'):
                            episode = params.getValue('episode')
                            if int(episode) > 0: mediaType = 'episode'
                        if imdbID and mediaType:
                            if mediaType == 'movie' or mediaType == 'tvshow':
                                metaInfo = meta.get_meta(self._mediaType, self.__sTitle, imdbID)
                            elif mediaType == 'season':
                                metaInfo = meta.get_seasons(TVShowTitle, imdbID, [str(season)])
                            elif mediaType == 'episode' and TVShowTitle:
                                metaInfo = meta.get_episode_meta(TVShowTitle, imdbID, str(season), str(episode))
                            if metaInfo and int(metaInfo['overlay']) == 6:
                                meta.change_watched(mediaType, name, imdbID, season=season, episode=episode)
                                xbmc.executebuiltin("XBMC.Container.Refresh")
                        else:
                            logger.info('Could not change watched status; imdbID or mediaType missing')
                except Exception as e:
                    logger.info(e)
                
    def onPlayBackEnded(self):
        logger.info('Playback completed')
        self.onPlayBackStopped()
        
class cPlayer:
      
    
    def clearPlayList(self):
        oPlaylist = self.__getPlayList()
        oPlaylist.clear()

    def __getPlayList(self):
        return xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

    def addItemToPlaylist(self, oGuiElement):
        oGui = cGui()
        oListItem =  oGui.createListItem(oGuiElement)
        self.__addItemToPlaylist(oGuiElement, oListItem)
	
    def __addItemToPlaylist(self, oGuiElement, oListItem):    
        oPlaylist = self.__getPlayList()	
        oPlaylist.add(oGuiElement.getMediaUrl(), oListItem )

    def startPlayer(self):
        logger.info('start player')
        xbmcPlayer = XstreamPlayer()

        while (not xbmc.abortRequested) & (not xbmcPlayer.streamFinished):
            if xbmcPlayer.isPlayingVideo():
                xbmcPlayer.playedTime = xbmcPlayer.getTime()
            xbmc.sleep(1000)
        return xbmcPlayer.streamSuccess
            
        
