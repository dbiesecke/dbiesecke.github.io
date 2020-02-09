import json
import urllib2



class PluginHelpers():
    def __init__(self):
        url=''

    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def getUnicodePage(self,url):
        req = urllib2.urlopen(url)
        content = ""
        if "content-type" in req.headers and "charset=" in req.headers['content-type']:
            encoding=req.headers['content-type'].split('charset=')[-1]
            content = unicode(req.read(), encoding)
        else:
            content = unicode(req.read(), "utf-8")
        return content

    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def parameters_string_to_dict(self,parameters):
        paramDict = {}
        if parameters:
            paramPairs = parameters[1:].split("&")
            for paramsPair in paramPairs:
                paramSplits = paramsPair.split('=')
                if (len(paramSplits)) == 2:
                    paramDict[paramSplits[0]] = paramSplits[1]
        return paramDict
#
#    ##########################################################################################################################
#    ##
#    ##########################################################################################################################
#    def writeLog(self, message, level=xbmc.LOGNOTICE):
#        try:
#            xbmc.log('[plugin.program.newscenter] %s' % ( message), level)
#        except Exception:
#            xbmc.log('[plugin.program.newscenter] %s' % ('Fatal: Message could not displayed'), xbmc.LOGERROR)
#
#    ##########################################################################################################################
#    ##
#    ##########################################################################################################################
#    def debug(self, message):
#        try:
#            xbmc.log('[plugin.program.newscenter] %s' % (message), xbmc.LOGDEBUG)
#        except Exception:
#            xbmc.log('[plugin.program.newscenter] %s' % ('Fatal: Message could not displayed'), xbmc.LOGERROR)
#
#
#    ##########################################################################################################################
#    ##
#    ##########################################################################################################################
#    def notifyOSD(self,header, message, icon=xbmcgui.NOTIFICATION_INFO, disp=4000, enabled=True):
#        if enabled:
#            OSD = xbmcgui.Dialog()
#            OSD.notification(header.encode('utf-8'), message.encode('utf-8'), icon, disp)
#



    class JSONRPC():
        def __init__(self):
            self.host     = '127.0.0.1'
            self.port     = '80'
    
        def getJsonResponse(self, host, port, method, params=None):
            url = 'http://%s:%s/jsonrpc' %(host, port)
            values ={}
            values['jsonrpc'] = '2.0'
            values['method'] = method
            if params is not None:
                values['params'] = params
            values['id'] = '1'
            headers = {'Content-Type':'application/json'}
    
            data = json.dumps(values)
    
            req = urllib2.Request(url, data, headers)
    
            response = urllib2.urlopen(req)
            return response.read()
    
        def Init(self, host, port):
            self.host = host
            self.port = port
    
        def PlayMedia(self, media):
            res = self.getJsonResponse(self.host, self.port,'Player.Open', { 'item':{'file':'%s' % media} })
            return res
    
        def PlaylistClear(self,num):
            res = self.getJsonResponse(self.host, self.port,'Playlist.Clear' , { 'playlistid' : num } )
            return res
    
        def PlaylistAdd(self,num,file):
            res = self.getJsonResponse(self.host, self.port, 'Playlist.Add' , { 'playlistid' : 0 , 'item' : {'file' : '%s' % file } } )
            return res
    
        def PlayPlaylist(self, id):
            res = self.getJsonResponse(self.host, self.port,'Player.Open', { 'item':{ 'playlistid':'%s' % id} })
            return res
   


ph = PluginHelpers.JSONRPC()
ph.PlayMedia('http://zdf0910-lh.akamaihd.net/i/de09_v1@392871/master.m3u8?dw=0') 
ph = PluginHelpers()
print ph.getUnicodePage('http://zdf0910-lh.akamaihd.net/i/de09_v1@392871/master.m3u8?dw=0')
