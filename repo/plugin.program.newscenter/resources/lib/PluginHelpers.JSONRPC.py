#!/usr/bin/python

import json
import urllib2

class PluginHelpers_JSONRPC():
    def __init__(self):
        self.host     = '127.0.0.1'
        self.port     = '80'
        #self.initdone = False

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
        print "Debug: %s" % (data) 
        req = urllib2.Request(url, data, headers)
    
        response = urllib2.urlopen(req)
        return response.read()

    def Init(self, host, port):
        self.host = host
        self.port = port
        self.initdone = True    

    def Prepare(self):
        if not self.initdone:
            self.host = "127.0.0.1"
            self.port = "80"

    def PlayMedia(self, media):
        #self.Prepare()
        res = self.getJsonResponse(self.host, self.port,'Player.Open', { 'item':{'file':'%s' % media} })
        return res
        
    def PlaylistClear(self,num):
        res = self.getJsonResponse(self.host, self.port,'Playlist.Clear' , { 'playlistid' : num } )
        return res

    def PlaylistAdd(self,num,file):
        res = self.getJsonResponse(self.host, self.port, 'Playlist.Add' , { 'playlistid' : 0 , 'item' : {'file' : '%s' % file } } )
        return res

    def PlayPlaylist(self, id):
        res = self.getJsonResponse(self.host, self.port,'Player.Open', { 'item':{'playlistid':'%s' % id} })
        return res

    def GetVolume(self):
        res = self.getJsonResponse(self.host, self.port,'Application.GetProperties', { 'properties': ['volume'] })
        return res

    def GetSystemInfo(self):
        res = self.getJsonResponse(self.host, self.port,'System.GetProperty', )
        return res

    def GetSystemTime(self):
        res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': ['System.Time'] })
        return res

    def GetProperty(self,prop):
        #res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': ['System.Time'] })
        res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': ['%s' % (prop)] })
        return res
    
    def GetAddons(self,prop):
        #res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': ['System.Time'] })
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddons',  )
        return res

    def GetAddonDetail(self,prop):
        #res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': ['System.Time'] })
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddonDetails',{ 'addonid': '%s' % (prop), 'properties':['name','version','summary','description','path','author','thumbnail','fanart','dependencies','broken','extrainfo','rating','enabled'] }  )
        return res

    def GetAddonNamebyID(self,addonid):
        #res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': ['System.Time'] })
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddonDetails',{ 'addonid': '%s' % (addonid), 'properties':['name'] }  )
        res = json.loads(res)
        res2 = res['result']['addon']['name']
        return res2

    def GetAddonVersionbyID(self,addonid):
        #res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': ['System.Time'] })
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddonDetails',{ 'addonid': '%s' % (addonid), 'properties':['version'] }  )
        res = json.loads(res)
        res2 = res['result']['addon']['version']
        return res2

    def GetAddonPropertybyID(self,addonid,prop):
        #res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': ['System.Time'] })
        p=[]
        p.append(prop)
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddonDetails',{ 'addonid': '%s' % (addonid), 'properties': p }  )
        res = json.loads(res)
        res2 = res['result']['addon'][prop]
        return res2

