#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import xbmc
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import random
import string
import json
import os
import ssl
from urllib import FancyURLopener, urlencode

addon = xbmcaddon.Addon()


class MainWindow(xbmcgui.WindowXML):
    ACTION_LEFT = 1
    ACTION_RIGHT = 2
    ACTION_UP = 3
    ACTION_DOWN = 4
    ACTION_PAGE_UP = 5
    ACTION_PAGE_DOWN = 6
    ACTION_SELECT_ITEM = 7
    ACTION_PARENT_DIR = 9
    ACTION_PREVIOUS_MENU = 10
    ACTION_SHOW_INFO = 11
    ACTION_NEXT_ITEM = 14
    ACTION_PREV_ITEM = 15

    ACTION_MOUSE_WHEEL_UP = 104
    ACTION_MOUSE_WHEEL_DOWN = 105
    ACTION_MOUSE_MOVE = 107

    KEY_NAV_BACK = 92
    KEY_CONTEXT_MENU = 117
    KEY_HOME = 159

    CHANNELS_PER_PAGE = 9

    XSERVER = 'https://xtream-editor.com'
    APPCODEURL = XSERVER + '/e2/get/newappid'
    SETTINGSURL = XSERVER + '/e2/get/settings/'

    PATH = xbmc.translatePath(addon.getAddonInfo('path'))

    VERSION = "2.95"

    __curfocus = 0

    def __new__(cls):
        return super(MainWindow, cls).__new__(cls, 'main.xml', addon.getAddonInfo('path'))

    def __init__(self):
        self.xappcode = addon.getSetting('appcode')
        self.lineid = addon.getSetting('lineid')
        self.qrcode = addon.getSetting('qrcode')
        self.m3uurl = addon.getSetting('m3uurl')
        self.epgurl = addon.getSetting('epgurl')
        self.sslcontext = ssl._create_unverified_context()

        if self.xappcode == "None":
            self.initApp()

    def urlopen(self, url, data=None):
        opener = XEOpener(context=self.sslcontext)
        if data is None:
            return opener.open(url)
        else:
            data = self.encodeParams(data)
            return opener.open(url, data)

    def encodeParams(self, params):
        return urlencode(params)

    def onInit(self):
        self.setFocusId(5000)
        self.setContent()

    def log(self, txt):
        if isinstance(txt, str):
            txt = txt.decode("utf-8")
            message = u'%s: %s' % ("XTREAM EDITOR", txt)
            xbmc.log(message.encode("utf-8"), xbmc.LOGDEBUG)

    def onAction(self, action):

        if action.getId() in [self.ACTION_PARENT_DIR, self.KEY_NAV_BACK, self.ACTION_PREVIOUS_MENU]:
            self.close()
            return
        if action.getId() == self.ACTION_DOWN:
            self.setFocusDown()
            return
        if action.getId() == self.ACTION_UP:
            self.setFocusUp()
            return

    def onClick(self, controlId):
        if controlId == 5000:
            self.getSettings()
            return
        if controlId == 5001:
            self.resetAction()
            return
        if controlId == 5002:
            self.close()
            return

    def setContent(self):
        if self.qrcode != "None":
            qr_c = self.getControl(4002)
            if qr_c:
                qr_c.setImage(self.qrcode, False)

        desc_c = self.getControl(1001)
        if desc_c:
            desc_c.setLabel(addon.getLocalizedString(50001) % (self.xappcode, self.lineid))

        code_c = self.getControl(1002)
        if code_c:
            code_c.setLabel(self.xappcode)

    def setFocusId(self, controlId):
        control = self.getControl(controlId)
        if control:
            self.setFocus(control)
            self.__curfocus = controlId

    def onFocus(self, controlId):
        pass

    def setFocusUp(self):
        new_id = int(self.__curfocus) - 1
        self.setFocusId(new_id)

    def setFocusDown(self):
        new_id = int(self.__curfocus) + 1
        self.setFocusId(new_id)

    def setPVRSettings(self):
        self.setContent()
        pvr = xbmcaddon.Addon(id="pvr.iptvsimple")

        m3u = addon.getSetting('m3uurl') + addon.getSetting('lineid')
        epg = addon.getSetting('epgurl') + addon.getSetting('lineid')

        pvr.setSetting('m3uUrl', m3u)
        pvr.setSetting('epgUrl', epg)
        pvr.setSetting('epgPathType', "1")
        pvr.setSetting('m3uPathType', "1")

        dialog = xbmcgui.Dialog()
        dialog.notification('XTREAM EDITOR', addon.getLocalizedString(50005), xbmcgui.NOTIFICATION_INFO, 5000)
        self.setContent()

    def initApp(self):
        self.log("initApp")
        try:
            params = {'version': self.VERSION}
            r = self.urlopen(self.APPCODEURL, params)
            self.log(r.getcode())
            if r.getcode() == 200:
                jsondata = r.read()
                d = json.loads(jsondata)
                xecode = d["xresult"]["appid"]
                qrurl = d["xresult"]["qrcode"]
                self.xappcode = xecode
                addon.setSetting('appcode', self.xappcode)
                self.qrcode = qrurl
                addon.setSetting('qrcode', self.qrcode)
                r.close()
                return True
            else:
                self.log("R CODE <> 200")
                r.close()
        except Exception as inst:
            self.log(inst)
            pass

    def getSettings(self):
        try:
            params = {'version': self.VERSION}
            r = self.urlopen(self.SETTINGSURL + self.xappcode, params)
            if r.getcode() == 200:
                jsondata = r.read()
                d = json.loads(jsondata)
                self.lineid = d["xresult"]["lineid"]
                self.m3uurl = d["xresult"]["m3upath"]
                self.epgurl = d["xresult"]["epgpath"]

                addon.setSetting('lineid', self.lineid)
                addon.setSetting('m3uurl', self.m3uurl)
                addon.setSetting('epgurl', self.epgurl)

                dialog = xbmcgui.Dialog()
                if self.lineid != '0':
                    ret = dialog.yesno('XTREAM EDITOR', addon.getLocalizedString(50003))
                    if ret:
                        self.setPVRSettings()
                else:
                    dialog.notification('XTREAM EDITOR', addon.getLocalizedString(50004), xbmcgui.NOTIFICATION_WARNING,
                                        5000)
            else:
                pass
        except:
            pass

    def resetAction(self):
        self.lineid = "None"
        self.qrcode = "None"
        self.m3uurl = "None"
        self.epgurl = "None"
        self.xappcode = "None"
        addon.setSetting('appcode', self.xappcode)
        addon.setSetting('lineid', self.lineid)
        addon.setSetting('m3uurl', self.m3uurl)
        addon.setSetting('epgurl', self.epgurl)
        addon.setSetting('qrcode', self.qrcode)
        self.initApp()
        self.setContent()


class XEOpener(FancyURLopener):
    version = 'KODI - XE 2.95'


if __name__ == '__main__':
    win = MainWindow()
    win.doModal()
    del win
    sys.modules.clear()
