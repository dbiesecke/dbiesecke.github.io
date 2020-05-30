from xbmcswift2 import Plugin
import re
import requests
import xbmc,xbmcaddon,xbmcvfs,xbmcgui
import xbmcplugin
import base64
import random
import urllib,urlparse
import time,datetime,calendar
import threading
import subprocess
import json
import os,os.path
import stat
import platform
import pickle
#import lzma
from HTMLParser import HTMLParser
from rpc import RPC
from bs4 import BeautifulSoup
import collections
import operator
import gzip
import StringIO

###
import sys
import string
import ssl
from urllib import FancyURLopener, urlencode


plugin = Plugin()
big_list_view = False

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

    #VERSION = "2.95"

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
        self.setFocusId(6000)
        self.setContent()

    def log(self, txt):
        if isinstance(txt, str):
            txt = txt.decode("utf-8")
            message = u'%s: %s' % ("XTREAM EDITOR", txt)
            #xbmc.log(message.encode("utf-8"), xbmc.LOGDEBUG)

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
     
        if controlId == 6000:
            self.getSettings()
            return
        if controlId == 6001:
            self.resetAction()
            return
        if controlId == 6002:
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
            #self.setFocus(control)
            self.__curfocus = controlId

    def onFocus(self, controlId):
        pass

    def setFocusUp(self):
        new_id = int(self.__curfocus) - 1
        #self.setFocusId(new_id)

    def setFocusDown(self):
        new_id = int(self.__curfocus) + 1
        #self.setFocusId(new_id)

    def setPVRSettings(self):
        #self.setContent()
       #pvr = xbmcaddon.Addon(id="pvr.iptvsimple")

            
        #which = xbmcgui.Dialog().select('M3U List',urls)
        #if which == -1:
            #return
        #url = urls[which]
        #if url:
            #url = url.replace("blob","raw")
            #urlname = url.replace("kodijnk22/kodinerds-iptv/raw/master/iptv/kodi","")
            #log(url)
            #name = xbmcgui.Dialog().input(url,url)
            #if name:
                
        #pvr.setSetting('m3uUrl', m3u)
        #pvr.setSetting('epgUrl', epg)
        #pvr.setSetting('epgPathType', "1")
        #pvr.setSetting('m3uPathType', "1")

        dialog = xbmcgui.Dialog()
        dialog.notification('XTREAM EDITOR', addon.getLocalizedString(50005), xbmcgui.NOTIFICATION_INFO, 5000)
        self.setContent()

    def initApp(self):
        self.log("initApp")
        try:
            params = {'version': 'KODI - XE 2.95'}
            r = self.urlopen(self.APPCODEURL, params)
            r.getcode()
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
                #self.log("R CODE <> 200")
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


def decode(x):
    try: return x.decode("utf8")
    except: return x

def addon_id():
    return xbmcaddon.Addon().getAddonInfo('id')

#def log(v):
    #xbmc.log(repr(v),xbmc.LOGERROR)

#log(sys.argv)

def profile():
    return xbmcaddon.Addon().getAddonInfo('profile')

def get_icon_path(icon_name):
    if plugin.get_setting('user.icons') == "true":
        user_icon = "special://profile/addon_data/%s/icons/%s.png" % (addon_id(),icon_name)
        if xbmcvfs.exists(user_icon):
            return user_icon
    return "special://home/addons/%s/resources/img/%s.png" % (addon_id(),icon_name)

def remove_formatting(label):
    label = re.sub(r"\[/?[BI]\]",'',label)
    label = re.sub(r"\[/?COLOR.*?\]",'',label)
    return label

def escape( str ):
    str = str.replace("&", "&amp;")
    str = str.replace("<", "&lt;")
    str = str.replace(">", "&gt;")
    str = str.replace("\"", "&quot;")
    return str

def unescape( str ):
    str = str.replace("&lt;","<")
    str = str.replace("&gt;",">")
    str = str.replace("&quot;","\"")
    str = str.replace("&amp;","&")
    return str


#@plugin.cached(TTL=plugin.get_setting('ttl',int))
def get_directory(media,path):
    try:
        response = RPC.files.get_directory(media=media, directory=path, properties=["thumbnail"])
        #log(response)
        return response
    except Exception as e:
        #log(e)
        return {"files":[]}


@plugin.route('/folder/<path>/<label>')
def folder(path,label):
    label = label.decode("utf8")
    media = "video"
    response = get_directory(media,path)
    files = response["files"]
    dir_items = []
    file_items = []
    for f in files:
        file_label = remove_formatting(f['label'])
        url = f['file']
        thumbnail = f['thumbnail']
        if not thumbnail:
            thumbnail = get_icon_path('unknown')

        if f['filetype'] == 'directory':
            if media == "video":
                window = "10025"
            elif media in ["music","audio"]:
                window = "10502"
            else:
                window = "10001"
            context_items = []
            context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add All Streams', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_all_folder, path=url, label=file_label.encode("utf8")))))
            context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Subscribe All Streams', 'XBMC.RunPlugin(%s)' % (plugin.url_for(subscribe_all_folder, path=url, label=file_label.encode("utf8")))))

            dir_label = "[B]%s[/B]" % file_label

            dir_items.append({
                'label': dir_label,
                'path': plugin.url_for('folder', path=url, label=file_label.encode("utf8")),
                'thumbnail': f['thumbnail'],
                'context_menu': context_items,
            })
        else:
            record_label = "[%s] %s" % (label,file_label)


            context_items = []
            context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add Stream', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_folder_stream, path=url, label=label.encode("utf8"), name=file_label.encode("utf8"),  thumbnail=f['thumbnail']))))
            context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add Search', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_folder_search, path=path, label=label.encode("utf8"), name=file_label.encode("utf8"),  thumbnail=f['thumbnail']))))

            display_label = "%s" % file_label

            file_items.append({
                'label': display_label,
                'path': url,
                'thumbnail': f['thumbnail'],
                'context_menu': context_items,
                'is_playable': True,
                'info_type': 'Video',
                'info':{"mediatype": "episode", "title": file_label}
            })

    return sorted(dir_items, key=lambda k: remove_formatting(k["label"]).lower()) + sorted(file_items, key=lambda k: remove_formatting(k["label"]).lower())


@plugin.route('/folder_search/<path>/<name>')
def folder_search(path,name):
    media = "video"
    response = get_directory(media,path)
    files = response["files"]
    dir_items = []
    file_items = []
    items = []
    for f in files:
        file_label = remove_formatting(f['label'])
        url = f['file']
        thumbnail = f['thumbnail']
        if not thumbnail:
            thumbnail = get_icon_path('unknown')

        if f['filetype'] == 'file':
            if re.search(name,file_label,flags=re.I):
                items.append((file_label,url))
    if items:
        if len(items) == 1:
            plugin.set_resolved_url(items[0][1])
        else:
            names = [x[0] for x in items]
            select = xbmcgui.Dialog().select(name,names)
            if select != -1:
                url = items[select][1]
                plugin.set_resolved_url(url)

@plugin.route('/m3u_search/<path>/<name>')
def m3u_search(path,name):
    data = get_data(path) or ""
    channels = re.findall('((#EXTINF.*?)\r?\n(.*?)\r?\n)', data, flags=(re.I|re.DOTALL|re.MULTILINE))
    items = []
    for channel,info,path in channels:
        #log(url)
        channel_name = None
        split = info.rsplit(',',1)
        #log((info,split))
        if len(split) == 2:
            channel_name = split[1]

            if re.search(name,channel_name,flags=re.I):
                items.append((channel_name,path))
    if items:
        if len(items) == 1:
            plugin.set_resolved_url(items[0][1])
        else:
            names = [x[0] for x in items]
            select = xbmcgui.Dialog().select(name,names)
            if select != -1:
                url = items[select][1]
                plugin.set_resolved_url(url)


@plugin.route('/m3u/<url>/<name>')
def m3u(url,name):
    data = get_data(url) or ""

    channels = re.findall('((#EXTINF.*?)\r?\n(.*?)\r?\n)', data, flags=(re.I|re.DOTALL|re.MULTILINE))
    items = []
    #log(channels)
    for channel,info,path in channels:
        #log(url)
        channel_name = None
        split = info.rsplit(',',1)
        #log((info,split))
        if len(split) == 2:
            channel_name = split[1]
        id = ""
        match = re.search('tvg-id="(.*?)"',info,flags=re.I)
        if match:
            id = match.group(1)
        group = ""
        match = re.search('group-title="(.*?)"',info,flags=re.I)
        if match:
            group = match.group(1)
        context_items = []
        #log(channel)
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add Stream', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_m3u_stream, channel=channel))))
        if channel_name:
            context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add Search', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_m3u_search, path=url, label=name, name=channel_name, thumbnail="none"))))
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add Group', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_m3u_group, url=url, group=group))))
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Subscribe Group', 'XBMC.RunPlugin(%s)' % (plugin.url_for(subscribe_m3u_group, url=url, group=group, name=name))))
        items.append({
            'label':"%s - [COLOR dimgray]%s[/COLOR] - %s" % (channel_name,id,group),
            'path' : path,
            'is_playable': True,
            'info_type': 'Video',
            'info':{"title": channel_name},
            'context_menu': context_items,
        })
    return items


@plugin.route('/epg/<url>/<name>')
def epg(url,name):
    data = get_data(url) or ""

    channels = re.findall('<channel.*?channel>', data, flags=(re.I|re.DOTALL|re.MULTILINE))
    items = []
    #log(channels)
    for channel in channels:
        channel_name = ""
        match = re.search('<display-name.*?>(.*?)<',channel, flags=(re.I|re.DOTALL|re.MULTILINE))
        if match:
            channel_name = match.group(1)
        id = ""
        match = re.search('id="(.*?)"',channel, flags=(re.I|re.DOTALL|re.MULTILINE))
        if match:
            id = match.group(1)
        context_items = []
        #log(channel)
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add Channel', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_epg_channel, channel=channel, name=name, url=url))))
        items.append({
            'label': "%s - [COLOR dimgray]%s[/COLOR]" % (channel_name,id),
            #'path' : path,
            'is_playable': True,
            'info_type': 'Video',
            'info':{"title": channel_name},
            'context_menu': context_items,
        })
    return items


@plugin.route('/play/<url>')
def play(url):
    xbmc.Player().play(url)


@plugin.route('/streams')
def streams():
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/channels.tsv'
    data = get_data(filename) or ""
    ids = [x.split('\t')[4] for x in data.splitlines() if x.startswith('CHANNEL')]
    #log(ids)
    #"special://home/addons/%s/resources/img/%s.png"
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/streams.m3u8'

 #   filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/streams.m3u8'
    data = get_data(filename) or ""
    channels = re.findall('((#EXTINF.*?)\r?\n(.*?)\r?\n)', data, flags=(re.I|re.DOTALL|re.MULTILINE))
    items = []
    #log(channels)
    for channel,info,url in channels:
        #log(url)
        name = None
        split = info.rsplit(',',1)
        #log((info,split))
        if len(split) == 2:
            name = split[1]
        color = "red"
        id = ""
        match = re.search('tvg-id="(.*?)"',info,flags=re.I)
        if match:
            id = match.group(1)
            if id in ids:
                color = "green"
        group = ""
        match = re.search('group-title="(.*?)"',info,flags=re.I)
        if match:
            group = match.group(1)
        context_items = []

        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Select EPG id', 'XBMC.RunPlugin(%s)' % (plugin.url_for(select_stream_id, id=id, name=name.encode("utf8")))))
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Play', 'XBMC.RunPlugin(%s)' % (plugin.url_for(play, url=url))))

        items.append({
            'label':"%s - [COLOR %s]%s[/COLOR] - %s" % (name,color,id,group),
            'path' : plugin.url_for(select_stream_id_list, id=id),
            #'is_playable': True,
            #'info_type': 'Video',
            #'info':{"title": name},
            'context_menu': context_items,
        })
    return items


@plugin.route('/template')
def template():
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    data = get_data(filename) or ""
    channels = re.findall('((#EXTINF.*?)\r?\n(.*?)\r?\n)', data, flags=(re.I|re.DOTALL|re.MULTILINE))
    items = []
    #log(channels)
    for channel,info,url in channels:
        #log(url)
        name = None
        split = info.rsplit(',',1)
        #log((info,split))
        if len(split) == 2:
            name = split[1]
        id = ""
        match = re.search('tvg-id="(.*?)"',info,flags=re.I)
        if match:
            id = match.group(1)
        group = ""
        match = re.search('group-title="(.*?)"',info,flags=re.I)
        if match:
            group = match.group(1)
        context_items = []
        #log(channel)
        path = url
        playable = True
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Move Stream', 'XBMC.RunPlugin(%s)' % (plugin.url_for(move_stream, channel=channel))))
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Remove Stream', 'XBMC.RunPlugin(%s)' % (plugin.url_for(remove_stream, channel=channel))))
        if name != "SUBSCRIBE":
            context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Edit Name', 'XBMC.RunPlugin(%s)' % (plugin.url_for(edit_stream_name, channel=channel))))
            context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Edit id', 'XBMC.RunPlugin(%s)' % (plugin.url_for(edit_stream_id, channel=channel))))
            context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Edit tvg-name', 'XBMC.RunPlugin(%s)' % (plugin.url_for(edit_stream_tvg_name, channel=channel))))
            context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Edit Group', 'XBMC.RunPlugin(%s)' % (plugin.url_for(edit_stream_group, channel=channel))))
        else:
            playable = False
            if not url.startswith('plugin'):
                path = plugin.url_for('m3u',url=url,name=id)

        #log(path)
        items.append({
            'label':"%s - [COLOR dimgray]%s[/COLOR] - %s" % (name,id,group),
            'path' : path,
            'is_playable': playable,
            'info_type': 'Video',
            'info':{"title": name},
            'context_menu': context_items,
        })
    return items

@plugin.route('/epg_template')
def epg_template():
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv'
    data = get_data(filename) or ""
    channels = [x for x in data.splitlines() if x]
    items = []
    #log(channels)
    for channel in channels:
        fields = channel.split('\t')
        type = fields[0]
        if type == "SUBSCRIBE":
            name = fields[1]
            url = fields[2]
            id = ""
            group = "SUBSCRIBE"
        elif type == "CHANNEL":
            url = fields[1]
            group = fields[2]
            name = fields[3]
            id = fields[4]

        context_items = []
        #log(channel)
        path = url
        playable = True

        items.append({
            'label':"%s - [COLOR dimgray]%s[/COLOR] - %s" % (name,id,group),
            #'path' : path,
            #'is_playable': playable,
            #'info_type': 'Video',
            #'info':{"title": name},
            'context_menu': context_items,
        })
    return items


@plugin.route('/channels')
def channels():
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/channels.tsv'
    data = get_data(filename) or ""
    channels = [x for x in data.splitlines() if x]
    items = []
    #log(channels)
    ids = []
    for channel in channels:
        fields = channel.split('\t')
        type = fields[0]
        if type == "SUBSCRIBE":
            name = fields[1]
            url = fields[2]
            id = ""
            group = "SUBSCRIBE"
        elif type == "CHANNEL":
            url = fields[1]
            group = fields[2]
            name = fields[3]
            id = fields[4]

        if id in ids:
            color = "red"
        else:
            color = "green"
        ids.append(id)


        context_items = []
        #log(channel)
        path = url
        playable = True

        #log(path)
        items.append({
            'label':"%s - [COLOR %s]%s[/COLOR] - %s" % (name,color,id,group),
            #'path' : path,
            #'is_playable': playable,
            #'info_type': 'Video',
            #'info':{"title": name},
            'context_menu': context_items,
        })
    return sorted(items, key=lambda k:k["label"].lower())

def windows():
    if os.name == 'nt':
        return True
    else:
        return False


def android_get_current_appid():
    with open("/proc/%d/cmdline" % os.getpid()) as fp:
        return fp.read().rstrip("\0")


def busybox_location():
    busybox_src = xbmc.translatePath(plugin.get_setting('busybox'))

    if xbmc.getCondVisibility('system.platform.android'):
        busybox_dst = '/data/data/%s/busybox' % android_get_current_appid()
        #log((busybox_dst,xbmcvfs.exists(busybox_dst)))
        if not xbmcvfs.exists(busybox_dst) and busybox_src != busybox_dst:
            xbmcvfs.copy(busybox_src, busybox_dst)

        busybox = busybox_dst
    else:
        busybox = busybox_src

    if busybox:
        try:
            st = os.stat(busybox)
            if not (st.st_mode & stat.S_IXUSR):
                try:
                    os.chmod(busybox, st.st_mode | stat.S_IXUSR)
                except:
                    pass
        except:
            pass
    if xbmcvfs.exists(busybox):
        return busybox
    else:
        xbmcgui.Dialog().notification("xmltv Meld","busybox not found",xbmcgui.NOTIFICATION_ERROR)


#@plugin.cached(TTL=60)
def get_data(url):
    if url:
        tempfile = xbmc.translatePath('special://home/addons/plugin.video.iptvsimple.addons/resources/tempfile')
        xbmcvfs.copy(url,tempfile)
        time.sleep(2)
        f = xbmcvfs.File(tempfile)
        data = f.read()
        f.close()

        if url.endswith('.xz'):
            filename = xbmc.translatePath('special://home/addons/plugin.video.iptvsimple.addons/resources/temp.xml')
            f = open(filename,"w")
            subprocess.call([busybox_location(),"xz","-dc",tempfile],stdout=f,shell=windows())
            f.close()
            time.sleep(2)
            data = xbmcvfs.File(filename,'r').read()
        else:
            magic = data[:3]
            if magic == "\x1f\x8b\x08":
                compressedFile = StringIO.StringIO()
                compressedFile.write(data)
                compressedFile.seek(0)
                decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
                data = decompressedFile.read()

        if data:
            return data + '\n'
    else:
        return

@plugin.route('/add_all_streams/<url>')
def add_all_streams(url):
    data = get_data(url)
    if not data:
        return
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"
    channels = re.findall('#EXTINF.*?\r?\n.*?\r?\n', data, flags=(re.I|re.DOTALL|re.MULTILINE))
    for channel in channels:
        original += channel
    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()

@plugin.route('/add_all_channels/<url>/<name>')
def add_all_channels(url,name):
    data = get_data(url)
    if not data:
        return
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv'
    original = get_data(filename) or ""
    #log(original)
    channels = re.findall('<channel.*?channel>', data, flags=(re.I|re.DOTALL|re.MULTILINE))
    for channel in channels:
        channel_name = ""
        match = re.search('<display-name.*?>(.*?)<',channel, flags=(re.I|re.DOTALL|re.MULTILINE))
        if match:
            channel_name = match.group(1)
        id = ""
        match = re.search('id="(.*?)"',channel, flags=(re.I|re.DOTALL|re.MULTILINE))
        if match:
            id = match.group(1)
        line = "CHANNEL\t%s\t%s\t%s\t%s\n" % (url,name,channel_name,id)
        #log(line)
        original += line
    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()
    xbmcgui.Dialog().notification("IPTV Addons","finished adding channels",sound=False)

@plugin.route('/add_m3u_group/<url>/<group>')
def add_m3u_group(url,group):
    data = get_data(url)
    if not data:
        return
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"
    channels = re.findall('#EXTINF.*?\r?\n.*?\r?\n', data, flags=(re.I|re.DOTALL|re.MULTILINE))
    for channel in channels:
        channel_group = ""
        match = re.search('group-title="(.*?)"',channel,flags=re.I)
        if match:
            channel_group = match.group(1)
        if channel_group == group:
            original += channel
    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()


@plugin.route('/add_all_folder/<path>/<label>')
def add_all_folder(path,label):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"

    match = re.search('plugin://(.*?)/',path)
    if match:
        plugin = match.group(1)
        plugin_name = xbmcaddon.Addon(plugin).getAddonInfo('name')
        label = "%s - %s" % (plugin_name,label)

    media = "video"
    response = get_directory(media,path)
    files = response["files"]
    dir_items = []
    file_items = []
    for f in files:
        file_label = remove_formatting(f['label'])
        url = f['file']
        thumbnail = f['thumbnail']
        if not thumbnail:
            thumbnail = get_icon_path('unknown')
        if f['filetype'] == 'file':
            channel = '#EXTINF:-1 tvg-name="%s" tvg-id="%s" tvg-logo="%s" group-title="%s",%s\n%s\n' % (file_label,file_label,thumbnail,label,file_label,url)
            original += channel.encode("utf8")

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()

@plugin.route('/subscribe_all_folder/<path>/<label>')
def subscribe_all_folder(path,label):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"

    match = re.search('plugin://(.*?)/',path)
    if match:
        plugin = match.group(1)
        plugin_name = xbmcaddon.Addon(plugin).getAddonInfo('name')
        label = "%s - %s" % (plugin_name,label)

    channel = '#EXTINF:-1 group-title="%s",SUBSCRIBE\n%s\n' % (label,path)
    original += channel

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()


@plugin.route('/add_folder_stream/<path>/<label>/<name>/<thumbnail>')
def add_folder_stream(path,label,name,thumbnail):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"

    match = re.search('plugin://(.*?)/',path)
    if match:
        addon = match.group(1)
        addon_name = xbmcaddon.Addon(addon).getAddonInfo('name')
        label = "%s - %s" % (addon_name,label)

    channel = '#EXTINF:-1 tvg-name="%s" tvg-id="%s" tvg-logo="%s" group-title="%s",%s\n%s\n' % (name,name,thumbnail,label,name,path)
    original += channel.encode("utf8")

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()

@plugin.route('/add_folder_search/<path>/<label>/<name>/<thumbnail>')
def add_folder_search(path,label,name,thumbnail):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"

    match = re.search('plugin://(.*?)/',path)
    if match:
        addon = match.group(1)
        addon_name = xbmcaddon.Addon(addon).getAddonInfo('name')
        label = "%s - %s" % (addon_name,label)

    new_name = xbmcgui.Dialog().input('%s (regex)' % (name),name)
    if not new_name:
        return
    name = new_name

    path = plugin.url_for('folder_search',name=name,path=path)

    channel = '#EXTINF:-1 tvg-name="%s" tvg-id="%s" tvg-logo="%s" group-title="%s",%s\n%s\n' % (name,name,thumbnail,label,name,path)
    original += channel.encode("utf8")

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()
#plugin.video.iptvsimple.addons/streams.m3u8
@plugin.route('/add_m3u_search/<path>/<label>/<name>/<thumbnail>')
def add_m3u_search(path,label,name,thumbnail):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(path) or "#EXTM3U\n"


    new_name = xbmcgui.Dialog().input('%s (regex)' % (name),name)
    if not new_name:
        return
    name = new_name

    path = plugin.url_for('m3u_search',name=name,path=path)

    channel = '#EXTINF:-1 tvg-name="%s" tvg-id="%s" tvg-logo="%s" group-title="%s",%s\n%s\n' % (name,name,thumbnail,label,name,path)
    original += channel.encode("utf8")

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()


@plugin.route('/add_m3u_stream/<channel>')
def add_m3u_stream(channel):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"

    original += channel #.encode("utf8")

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()

@plugin.route('/add_epg_channel/<channel>/<name>/<url>')
def add_epg_channel(channel,name,url):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv'
    original = get_data(filename) or ""

    channel_name = ""
    match = re.search('<display-name.*?>(.*?)<',channel, flags=(re.I|re.DOTALL|re.MULTILINE))
    if match:
        channel_name = match.group(1)
    id = ""
    match = re.search('id="(.*?)"',channel, flags=(re.I|re.DOTALL|re.MULTILINE))
    if match:
        id = match.group(1)
    line = "CHANNEL\t%s\t%s\t%s\t%s\n" % (url,name,channel_name,id)
    #log(line)
    original += line

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()

@plugin.route('/remove_stream/<channel>')
def remove_stream(channel):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"

    original = original.replace(channel,'')

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/move_stream/<channel>')
def move_stream(channel):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"

    original = original.replace(channel,'')

    channels = re.findall('((#EXTINF.*?)\r?\n(.*?)\r?\n)', original, flags=(re.I|re.DOTALL|re.MULTILINE))
    items = []
    #log(channels)
    for new_channel,info,url in channels:
        #log(url)
        name = None
        split = info.rsplit(',',1)
        #log((info,split))
        if len(split) == 2:
            name = split[1]
            items.append((name,new_channel))
    select = xbmcgui.Dialog().select('%s (move after)',[x[0] for x in items])
    if select == -1:
        return
    original = original.replace(items[select][1],items[select][1]+channel)

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()
    xbmc.executebuiltin('Container.Refresh')

@plugin.route('/edit_stream_name/<channel>')
def edit_stream_name(channel):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"

    new_channel = None
    match = re.search('(#EXTINF.*?)\r?\n(.*?)\r?\n', channel, flags=(re.I|re.DOTALL|re.MULTILINE))
    if match:
        info = match.group(1)
        url = match.group(2)
        name = None
        split = info.rsplit(',',1)
        #log((info,split))
        if len(split) == 2:
            name = split[1]
            extinf = split[0]
            new_name = xbmcgui.Dialog().input('Edit',name)
            if new_name:
                new_info = "%s,%s" %(extinf,new_name)
                new_channel = channel.replace(info,new_info)

    #return
    if not new_channel:
        return

    original = original.replace(channel,new_channel)

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()

@plugin.route('/edit_stream_id/<channel>')
def edit_stream_id(channel):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"

    new_channel = None
    match = re.search('(#EXTINF.*?)\r?\n(.*?)\r?\n', channel, flags=(re.I|re.DOTALL|re.MULTILINE))
    if match:
        info = match.group(1)
        url = match.group(2)
        name = None
        split = info.rsplit(',',1)
        #log((info,split))
        if len(split) == 2:
            name = split[1]
            extinf = split[0]
            match = re.search('tvg-id="(.*?)"',extinf,flags=re.I)
            if match:
                tvg_id = match.group(0)
                id = match.group(1)
                new_id = xbmcgui.Dialog().input('Edit id',id)
                if new_id:
                    new_channel = channel.replace(tvg_id,tvg_id.replace(id,new_id))

    #return
    if not new_channel:
        return

    original = original.replace(channel,new_channel)

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()

@plugin.route('/remove_m3u_id_rule')
def remove_m3u_id_rule():
    ids = plugin.get_storage('ids')
    new_ids = [(x,ids[x]) for x in sorted(ids)]
    labels = ["%s => %s" % x for x in new_ids]
    selection = xbmcgui.Dialog().multiselect("remove id rules",labels)
    if selection == None:
        return
    for i in selection:
        id = new_ids[i][0]
        del ids[id]



@plugin.route('/select_stream_id/<id>/<name>')
def select_stream_id(id,name):
    lower_name = name.decode("utf8").lower()
    #TODO exact, partial, other
    ids = plugin.get_storage('ids')
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/channels.tsv'
    data = get_data(filename) or ""
    channels = [x.split('\t') for x in data.splitlines() if x.startswith('CHANNEL')]
    channels.sort(key=lambda k: k[3].lower())
    for channel in channels[:]:
        channel_name = channel[3].decode("utf8").lower()
        #log((channel_name,lower_name))
        if channel_name.startswith(lower_name) or lower_name.startswith(channel_name):
            #log((lower_name,channel_name,channel))
            channels.insert(0,channel)
    labels = ["[COLOR yellow]%s[/COLOR] - %s - %s" % (x[3],x[2],x[4]) for x in channels]
    select = xbmcgui.Dialog().select("%s [%s]" % (name,id),labels)
    if select == -1:
        return
    type,url,group,name,new_id = channels[select]
    #log((id,new_id))
    ids[id] = new_id

@plugin.route('/set_stream_id/<id>/<new_id>')
def set_stream_id(id,new_id):
    #TODO exact, partial, other
    ids = plugin.get_storage('ids')
    ids[id] = new_id
    xbmcgui.Dialog().notification(id,new_id,sound=False)

@plugin.route('/select_stream_id_list/<id>')
def select_stream_id_list(id):
    #TODO exact, partial, other
    ids = plugin.get_storage('ids')
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/channels.tsv'
    data = get_data(filename) or ""
    channels = [x.split('\t') for x in data.splitlines() if x.startswith('CHANNEL')]
    channels.sort(key=lambda k: k[3].lower())
    items = []
    for type,url,group,name,new_id in channels:
        items.append({
            'label': "[COLOR yellow]%s[/COLOR] - %s - %s" % (name,group,new_id),
            'path': plugin.url_for('set_stream_id',id=id,new_id=new_id)
        })
    return items

@plugin.route('/edit_stream_group/<channel>')
def edit_stream_group(channel):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"

    new_channel = None
    match = re.search('(#EXTINF.*?)\r?\n(.*?)\r?\n', channel, flags=(re.I|re.DOTALL|re.MULTILINE))
    if match:
        info = match.group(1)
        url = match.group(2)
        name = None
        split = info.rsplit(',',1)
        #log((info,split))
        if len(split) == 2:
            name = split[1]
            extinf = split[0]
            match = re.search('group-title="(.*?)"',extinf,flags=re.I)
            if match:
                tvg_id = match.group(0)
                id = match.group(1)
                new_id = xbmcgui.Dialog().input('Edit group',id)
                if new_id:
                    new_channel = channel.replace(tvg_id,tvg_id.replace(id,new_id))

    #return
    if not new_channel:
        return

    original = original.replace(channel,new_channel)

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()

@plugin.route('/edit_stream_tvg_name/<channel>')
def edit_stream_tvg_name(channel):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"

    new_channel = None
    match = re.search('(#EXTINF.*?)\r?\n(.*?)\r?\n', channel, flags=(re.I|re.DOTALL|re.MULTILINE))
    if match:
        info = match.group(1)
        url = match.group(2)
        name = None
        split = info.rsplit(',',1)
        #log((info,split))
        if len(split) == 2:
            name = split[1]
            extinf = split[0]
            match = re.search('tvg-name="(.*?)"',extinf,flags=re.I)
            if match:
                tvg_id = match.group(0)
                id = match.group(1)
                new_id = xbmcgui.Dialog().input('Edit tvg-name',id)
                if new_id:
                    new_channel = channel.replace(tvg_id,tvg_id.replace(id,new_id))

    #return
    if not new_channel:
        return

    original = original.replace(channel,new_channel)

    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()


@plugin.route('/update_streams/')
def update_streams():
    ids = plugin.get_storage('ids')
    #for x in ids:
        #log(("x",x,ids[x]))
    #log("update_stream")
    url = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    data = get_data(url)
    #log(data)
    if not data:
        return
    original = "#EXTM3U\n"
    channels = re.findall('((#EXTINF.*?)\r?\n(.*?)\r?\n)', data, flags=(re.I|re.DOTALL|re.MULTILINE))
    items = []
    #log(channels)
    for channel,info,url in channels:
        #log(url)
        name = None
        split = info.rsplit(',',1)
        #log((info,split))
        if len(split) == 2:
            name = split[1]
        id = ""
        match = re.search('tvg-id="(.*?)"',info,flags=re.I)
        if match:
            id = match.group(1)
        group = ""
        match = re.search('group-title="(.*?)"',info,flags=re.I)
        if match:
            group = match.group(1)
        if name == "SUBSCRIBE":
            if url.startswith('plugin'):
                match = re.search('group-title="(.*?)"',info,flags=re.I)
                if match:
                    label = match.group(1)

                media = "video"
                response = get_directory(media,url)
                files = response["files"]
                dir_items = []
                file_items = []
                for f in files:
                    file_label = remove_formatting(f['label'])
                    url = f['file']
                    thumbnail = f['thumbnail']
                    if not thumbnail:
                        thumbnail = get_icon_path('unknown')
                    if f['filetype'] == 'file':
                        channel = '#EXTINF:-1 tvg-name="%s" tvg-id="%s" tvg-logo="%s" group-title="%s",%s\n%s\n' % (file_label,file_label,thumbnail,label,file_label,url)
                        original += channel.encode("utf8")
            else:
                #log(url)
                data = get_data(url)
                new_channels = re.findall('#EXTINF.*?\r?\n.*?\r?\n', data, flags=(re.I|re.DOTALL|re.MULTILINE))
                if group:
                    for new_channel in new_channels:
                        match = re.search('group-title="(.*?)"',new_channel,flags=re.I)
                        if match:
                            new_group = match.group(1)
                            if new_group == group:
                                #log(group)
                                original += new_channel
                else:
                    for new_channel in new_channels:
                        #log(new_channel)
                        original += new_channel
        else:
            original += channel
    for id in ids:
        new_id = ids[id]
        original = original.replace('tvg-id="%s"' % id, 'tvg-id="%s"' % new_id)
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/streams.m3u8'
    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()
    xbmcgui.Dialog().notification("IPTV Addons","finished updating streams")
    time.sleep(2)
    RPC.addons.set_addon_enabled(addonid='pvr.iptvsimple', enabled=False)
    time.sleep(2)
    RPC.addons.set_addon_enabled(addonid='pvr.iptvsimple', enabled=True)


@plugin.route('/update_channels/')
def update_channels():

    url = 'special://home/addons/plugin.video.iptvsimple.addons/resources/ignores.json'
    f = xbmcvfs.File(url)
    data = f.read()
    f.close()
    try:
        ignores = json.loads(data)
    except:
        ignores = []

    url = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv'
    data = get_data(url)
    if not data:
        return
    original = ""
    channels = [x for x in data.splitlines() if x]
    items = []
    #log(channels)
    ids = []
    duplicates = []
    for channel in channels:
        fields = channel.split('\t')
        type = fields[0]
        if type == "SUBSCRIBE":
            name = fields[1]
            url = fields[2]
            id = ""
            group = "SUBSCRIBE"
            data = get_data(url) or ""
            new_channels = re.findall('<channel.*?channel>', data, flags=(re.I|re.DOTALL|re.MULTILINE))
            items = []
            #log(new_channels)
            for new_channel in new_channels:
                channel_name = ""
                match = re.search('<display-name.*?>(.*?)<',new_channel, flags=(re.I|re.DOTALL|re.MULTILINE))
                if match:
                    channel_name = match.group(1)
                id = ""
                match = re.search('id="(.*?)"',new_channel, flags=(re.I|re.DOTALL|re.MULTILINE))
                if match:
                    id = match.group(1)
                line = "CHANNEL\t%s\t%s\t%s\t%s\n" % (url,name,channel_name,id)
                if line not in ignores:
                    original += line
                    if id in ids:
                        duplicates.append(id)
                        #id = id + str(ids.count(id)+1)
                ids.append(id)

        elif type == "CHANNEL":
            url = fields[1]
            group = fields[2]
            name = fields[3]
            id = fields[4]
            channel = channel + '\n'
            if channel not in ignores:
                original += channel
                if id in ids:
                    duplicates.append(id)
                    #new_id = id + str(ids.count(id)+1)
                    #fields[4] = new_id
                    #channel = '\t'.join(fields)
                    #log((id,new_id,channel))

            ids.append(id)
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/channels.tsv'
    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/duplicates.json'
    f = xbmcvfs.File(filename,'w')
    f.write(json.dumps(duplicates))
    f.close()
    time.sleep(2)
    update_xml()
    xbmcgui.Dialog().notification("IPTV Addons","finished updating epg")
    time.sleep(2)
    RPC.addons.set_addon_enabled(addonid='pvr.iptvsimple', enabled=False)
    time.sleep(2)
    RPC.addons.set_addon_enabled(addonid='pvr.iptvsimple', enabled=True)

@plugin.route('/duplicates/')
def duplicates():
    url = 'special://home/addons/plugin.video.iptvsimple.addons/resources/channels.tsv'
    f = xbmcvfs.File(url)
    data = f.read()
    f.close()
    channels = [x.split('\t') for x in data.splitlines() if x.startswith('CHANNEL')]
    url = 'special://home/addons/plugin.video.iptvsimple.addons/resources/duplicates.json'
    f = xbmcvfs.File(url)
    data = f.read()
    f.close()
    try:
        dupes = json.loads(data)
    except:
        dupes = []
    ignores = []
    for dupe in sorted(dupes):
        #log(dupe)
        #log(channels)
        chans = [x for x in channels if x[4] == dupe]
        #log(chans)
        labels = ["%s - %s" % (x[2],x[3]) for x in chans]
        select = xbmcgui.Dialog().select(dupe,labels)
        if select == -1:
            return
        ignore = [x for i,x in enumerate(chans) if i != select]
        for i in ignore:
            type,url,name,channel_name,id = i
            line = "%s\t%s\t%s\t%s\t%s\n" % (type,url,name,channel_name,id)
            ignores.append(line)
    if not ignores:
        return
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/ignores.json'
    f = xbmcvfs.File(filename,'w')
    f.write(json.dumps(ignores))
    f.close()
    xbmcgui.Dialog().notification("IPTV Addons","updating epg")
    update_channels()


@plugin.route('/service')
def service():
    update_streams()
    update_channels()

@plugin.route('/disable_iptvsimple')
def disable_iptvsimple():
    RPC.addons.set_addon_enabled(addonid='pvr.iptvsimple', enabled=False)

@plugin.route('/enable_iptvsimple')
def enable_iptvsimple():
    RPC.addons.set_addon_enabled(addonid='pvr.iptvsimple', enabled=True)


def update_xml():
    url = 'special://home/addons/plugin.video.iptvsimple.addons/resources/channels.tsv'
    data = get_data(url)
    if not data:
        return
    tsv_channels = [x.split('\t') for x in data.splitlines() if x.startswith('CHANNEL')]
    #log(tsv_channels)
    urls = set()
    url_ids = collections.defaultdict(list)
    for type,url,group,name,id in tsv_channels:
        #log((type,url,group,name,id))
        urls.add(url)

        url_ids[url].append(id)

    xml_channels = collections.defaultdict(dict)
    xml_programmes = collections.defaultdict(list)
    for url in urls:
        data = get_data(url)
        channels = re.findall('<channel.*?channel>', data, flags=(re.I|re.DOTALL|re.MULTILINE))
        for channel in channels:
            id = ""
            match = re.search('id="(.*?)"',channel, flags=(re.I|re.DOTALL|re.MULTILINE))
            if match:
                id = match.group(1)
                if id in url_ids[url]:
                    xml_channels[url][id] = channel
        programmes = re.findall('<programme.*?programme>', data, flags=(re.I|re.DOTALL|re.MULTILINE))
        for programme in programmes:
            id = ""
            match = re.search('channel="(.*?)"',programme, flags=(re.I|re.DOTALL|re.MULTILINE))
            if match:
                id = match.group(1)
                if id in url_ids[url]:
                    xml_programmes[url].append(programme)

    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/xmltv.xml'
    f = xbmcvfs.File(filename,'w')
    f.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE tv SYSTEM "xmltv.dtd">
<tv source-info-name="test" generator-info-name="test" generator-info-url="test">'''+'\n')
    for type,url,group,name,id in tsv_channels:
        channel = xml_channels[url][id]
        f.write(channel+'\n')
    for url in urls:
        programmes = xml_programmes[url]
        for programme in programmes:
            f.write(programme+'\n')
    f.write('</tv>')
    f.close()

@plugin.route('/clear_streams/')
def clear_streams():
    tempfile = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8.1'
    f = xbmcvfs.File(tempfile)
    data = f.read()
    f.close()   

@plugin.route('/backup_streams/')
def backup_streams():
    tempfile = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    f = xbmcvfs.File(tempfile)
    data = f.read()
    f.close()   
    
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8.bak'
    f = xbmcvfs.File(filename,'w')
    f.write(data)
    f.close()
    
    tempfile = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv'
    f = xbmcvfs.File(tempfile)
    data = f.read()
    f.close()   
    
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv.bak'
    f = xbmcvfs.File(filename,'w')
    f.write(data)
    f.close()   
    
@plugin.route('/backup_install/')
def backup_install():
    tempfile = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8.bak'
    f = xbmcvfs.File(tempfile)
    data = f.read()
    f.close()   
    if  not data:
        return    
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    f = xbmcvfs.File(filename,'w')
    f.write(data)
    f.close()
    
    tempfile = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv.bak'
    f = xbmcvfs.File(tempfile)
    data = f.read()
    f.close()   
    if not data:
        return     
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv'
    f = xbmcvfs.File(filename,'w')
    f.write(data)
    f.close() 
    
@plugin.route('/default_streams/')
def default_streams():
    tempfile = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8.1'
    f = xbmcvfs.File(tempfile)
    data = f.read()
    f.close()   
    
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    f = xbmcvfs.File(filename,'w')
    f.write(data)
    f.close()
    
@plugin.route('/default_channels/')
def default_channels():
    tempfile = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv.1'
    f = xbmcvfs.File(tempfile)
    data = f.read()
    f.close()   
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv'
    f = xbmcvfs.File(filename,'w')
    f.write(data)
    f.close()
    
    
@plugin.route('/clear_channels/')
def clear_channels():
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv'
    f = xbmcvfs.File(filename,'w')
    f.close()


@plugin.route('/subscribe_all_streams/<url>/<name>')
def subscribe_all_streams(url,name):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"
    #channels = re.findall('#EXTINF.*?\r?\n.*?\r?\n', data, flags=(re.I|re.DOTALL|re.MULTILINE))
    channel = '#EXTINF:-1 tvg-id="%s",SUBSCRIBE\n%s\n' % (name,url)
    original += channel
    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()


@plugin.route('/subscribe_all_channels/<url>/<name>')
def subscribe_all_channels(url,name):
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.tsv'
    original = get_data(filename) or ""

    channel = 'SUBSCRIBE\t%s\t%s\n' % (name,url)
    original += channel
    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()

@plugin.route('/subscribe_m3u_group/<url>/<group>/<name>')
def subscribe_m3u_group(url,group,name):
    data = get_data(url)
    if not data:
        return
    filename = 'special://home/addons/plugin.video.iptvsimple.addons/resources/template.m3u8'
    original = get_data(filename) or "#EXTM3U\n"
    channels = re.findall('#EXTINF.*?\r?\n.*?\r?\n', data, flags=(re.I|re.DOTALL|re.MULTILINE))
    channel = '#EXTINF:-1 tvg-id="%s" group-title="%s",SUBSCRIBE\n%s\n' % (name,group,url)
    original += channel
    f = xbmcvfs.File(filename,'w')
    f.write(original)
    f.close()


@plugin.route('/m3u_playlists')
def m3u_playlists():
    m3us = plugin.get_storage('m3us')
    items = []
    for url,name in m3us.items():
        context_items = []
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add All Streams', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_all_streams,url=url))))
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Subscribe All Streams', 'XBMC.RunPlugin(%s)' % (plugin.url_for(subscribe_all_streams,url=url,name=name.encode("utf8")))))
        items.append({
            'label': name,
            'path': plugin.url_for('m3u',url=url, name=name),
            'context_menu': context_items,
        })

    return sorted(items, key=lambda k: remove_formatting(k["label"]).lower())


@plugin.route('/epg_sources')
def epg_sources():
    xappcode = addon.getSetting('appcode')
    lineid = addon.getSetting('lineid')
    m3uurl = addon.getSetting('m3uurl')
    epgurl = addon.getSetting('epgurl')
    sslcontext = ssl._create_unverified_context()


    epgs = plugin.get_storage('epgs')
    items = []
    context_items = []
    for url,name in epgs.items():
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add All Channels', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_all_channels,url=url,name=name.encode("utf8")))))
        context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Subscribe All Channels', 'XBMC.RunPlugin(%s)' % (plugin.url_for(subscribe_all_channels,url=url,name=name.encode("utf8")))))
        items.append({
            'label': name,
            'path': plugin.url_for('epg',url=url, name=name),
            'context_menu': context_items,
        })
        
    items.append(
    {
        'label': "Xtream-Editor EPG",
        'path': plugin.url_for('epg',url=addon.getSetting('epgurl') + addon.getSetting('lineid'), name=addon.getSetting('lineid')),
        'context_menu': context_items,
    }) 
        
        
    return sorted(items, key=lambda k: remove_formatting(k["label"]).lower())

@plugin.route('/add_iptvsimple_m3u')
def add_iptvsimple_m3u():
    m3us = plugin.get_storage('m3us')
    which = xbmcgui.Dialog().select('IPTV Simple Client M3U',["URL","File"])
    if which == -1:
        return
    if which == 0:
        url = xbmcaddon.Addon('pvr.iptvsimple').getSetting('m3uUrl')
        if url:
            name = xbmcgui.Dialog().input("Name","IPTV Simple Client URL")
            if name:
                m3us[url] = name
    elif which == 0:
        url = xbmcaddon.Addon('pvr.iptvsimple').getSetting('m3uPath')
        if url:
            name = xbmcgui.Dialog().input("Name","IPTV Simple Client File")
            if name:
                m3us[url] = name

@plugin.route('/add_iptvsimple_epg')
def add_iptvsimple_epg():
    epgs = plugin.get_storage('epgs')
    which = xbmcgui.Dialog().select('IPTV Simple Client epg',["URL","File"])
    if which == -1:
        return
    if which == 0:
        url = xbmcaddon.Addon('pvr.iptvsimple').getSetting('epgUrl')
        if url:
            name = xbmcgui.Dialog().input("Name","IPTV Simple Client URL")
            if name:
                epgs[url] = name
    elif which == 0:
        url = xbmcaddon.Addon('pvr.iptvsimple').getSetting('epgPath')
        if url:
            name = xbmcgui.Dialog().input("Name","IPTV Simple Client File")
            if name:
                epgs[url] = name

@plugin.route('/add_rytec_epg')
def add_rytec_epg():
    epgs = plugin.get_storage('epgs')

    base_url = 'http://rytec.ricx.nl/epg_data/'
    data = requests.get(base_url).text
    #log(data)
    urls = [x for x in re.findall('href="(rytec.*?)"',data)]

    which = xbmcgui.Dialog().select('IPTV Simple Client epg',urls)
    if which == -1:
        return
    url = urls[which]
    if url:
        name = xbmcgui.Dialog().input(url,url)
        log(name)
        if name:
            epgs[base_url+url] = name

@plugin.route('/add_psycotv')
def add_psycotv():
    urlstorage = plugin.get_storage('m3us')
    #https://github.com/jnk22/kodinerds-iptv/raw/master/iptv/kodi/kodi_radio.m3u
    base_url = 'http://psyco.tv/m3us2/'
    data = requests.get(base_url).text
    #log(data)
    urls = [x for x in re.findall('href="(.*\.m3u)"',data)]

    which = xbmcgui.Dialog().select('M3U List',urls)
    if which == -1:
        return
    url = urls[which]
    if url:
        name = xbmcgui.Dialog().input(url,url)
        if name:
            urlstorage[base_url+url] = url

@plugin.route('/add_kodinerds')
def add_kodinerds():
    urlstorage = plugin.get_storage('m3us')
    #https://github.com/jnk22/kodinerds-iptv/raw/master/iptv/kodi/kodi_radio.m3u
    base_url = 'https://github.com/jnk22/kodinerds-iptv/tree/master/iptv/kodi'
    data = requests.get(base_url).text
    #log(data)
    base_url = 'https://github.com'    
    urls = [x for x in re.findall('href="(.*\.m3u)"',data)]

    which = xbmcgui.Dialog().select('M3U List',urls)
    if which == -1:
        return
    url = urls[which]
    if url:
        url = url.replace("blob","raw")
        urlname = url.replace("kodijnk22/kodinerds-iptv/raw/master/iptv/kodi","")
        name = xbmcgui.Dialog().input(url,url)
        if name:
            urlstorage[base_url+urlname] = name
            
@plugin.route('/add_m3u_url')
def add_m3u_url():
    m3us = plugin.get_storage('m3us')
    url = xbmcgui.Dialog().input('M3U URL')
    if url:
        name = xbmcgui.Dialog().input("Name")
        if name:
            m3us[url] = name

@plugin.route('/add_m3u_file')
def add_m3u_file():
    m3us = plugin.get_storage('m3us')
    path = xbmcgui.Dialog().browseSingle(1, 'M3U', '', '', False, False)
    if path:
        name = xbmcgui.Dialog().input("Name")
        if name:
            m3us[path] = name

@plugin.route('/add_epg_url')
def add_epg_url():
    epgs = plugin.get_storage('epgs')
    url = xbmcgui.Dialog().input('epg URL')
    if url:
        name = xbmcgui.Dialog().input("Name")
        if name:
            epgs[url] = name

@plugin.route('/add_epg_file')
def add_epg_file():
    epgs = plugin.get_storage('epgs')
    path = xbmcgui.Dialog().browseSingle(1, 'epg', '', '', False, False)
    if path:
        name = xbmcgui.Dialog().input("Name")
        if name:
            epgs[path] = name

@plugin.route('/set_iptvsimple_m3u_file')
def set_iptvsimple_m3u_file():
    xbmcaddon.Addon('pvr.iptvsimple').setSetting('m3uPathType',"0")
    xbmcaddon.Addon('pvr.iptvsimple').setSetting('m3uPath',xbmc.translatePath('special://home/addons/plugin.video.iptvsimple.addons/resources/streams.m3u8'))

@plugin.route('/set_iptvsimple_epg_file')
def set_iptvsimple_epg_file():
    xbmcaddon.Addon('pvr.iptvsimple').setSetting('epgPathType',"0")
    xbmcaddon.Addon('pvr.iptvsimple').setSetting('epgPath',xbmc.translatePath('special://home/addons/plugin.video.iptvsimple.addons/resources/xmltv.xml'))

@plugin.route('/pair_xe')
def pair_xe():    
    win = MainWindow()
    #win.initApp()
    win.doModal()
    del win
    sys.modules.clear() 
   
@plugin.route('/sync_xe')
def sync_xe():    
    XSERVER = 'https://xtream-editor.com'
    APPCODEURL = XSERVER + '/e2/get/newappid'
    SETTINGSURL = XSERVER + '/e2/get/settings/'     
    try:
        params = {'version': 'KODI - XE 2.95'}
        #self.log(self.SETTINGSURL)
        xappcode = addon.getSetting('appcode')
        win = MainWindow()
        r = win.urlopen(SETTINGSURL + xappcode, params)
        if r.getcode() == 200:
            jsondata = r.read()
            d = json.loads(jsondata)
            lineid = d["xresult"]["lineid"]
            #self.m3uurl = d["xresult"]["m3upath"]
            #self.epgurl = d["xresult"]["epgpath"]

            addon.setSetting('lineid', d["xresult"]["lineid"])
            addon.setSetting('m3uurl', d["xresult"]["m3upath"])
            addon.setSetting('epgurl', d["xresult"]["epgpath"])

            dialog = xbmcgui.Dialog()
            if lineid != '0':
                ret = dialog.yesno('XTREAM EDITOR', addon.getLocalizedString(50003))
                if ret:
                    win.setPVRSettings()
            else:
                dialog.notification('XTREAM EDITOR', addon.getLocalizedString(50004), xbmcgui.NOTIFICATION_WARNING,
                                    5000)
    except Exception as inst:
        #self.log(inst)
        pass
 
    
    
@plugin.route('/')
def index():
    items = []
    
    
    context_items = []
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Sync with Xtream-Editor', 'XBMC.RunPlugin(%s)' % (plugin.url_for(sync_xe)))) 
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Pair with Xtream-Editor', 'XBMC.RunPlugin(%s)' % (plugin.url_for(pair_xe))))            
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add PsycoTV Playlist', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_psycotv))))        
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add Kodi Nerds', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_kodinerds))))    
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add IPTV Simple Client M3U', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_iptvsimple_m3u))))
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add M3U URL', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_m3u_url))))
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add M3U File', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_m3u_file))))
    items.append(
    {
        'label': "M3U Playlists",
        'path': plugin.url_for('m3u_playlists'),
        'thumbnail':get_icon_path('tv'),
        'context_menu': context_items,
    })
    xappcode = addon.getSetting('appcode')
    lineid = addon.getSetting('lineid')
    m3uurl = addon.getSetting('m3uurl')
    epgurl = addon.getSetting('epgurl')
    sslcontext = ssl._create_unverified_context()

    if lineid != "None":
        items.append(
        {
            'label': "Xtream-Editor Playlists",
            'path': plugin.url_for('m3u',url=addon.getSetting('m3uurl') + addon.getSetting('lineid'), name=addon.getSetting('lineid')),
            'thumbnail':get_icon_path('tv'),
            'context_menu': context_items,
        })
        
    context_items = []
    items.append(
    {
        'label': "Library",
        'path': plugin.url_for('folder',path="library://video",label="Library"),
        'thumbnail':get_icon_path('tv'),
        'context_menu': context_items,
    })
  
    context_items = []
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Set Default Streams', 'XBMC.RunPlugin(%s)' % (plugin.url_for(default_streams))))    
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Set Default Templates', 'XBMC.RunPlugin(%s)' % (plugin.url_for(default_channels))))    
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Backup Streams/Template', 'XBMC.RunPlugin(%s)' % (plugin.url_for(backup_streams))))      
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Streams/Template Backup install', 'XBMC.RunPlugin(%s)' % (plugin.url_for(backup_install))))                
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Clear', 'XBMC.RunPlugin(%s)' % (plugin.url_for(clear_streams))))
    items.append(
    {
        'label': "Stream Template",
        'path': plugin.url_for('template'),
        'thumbnail':get_icon_path('tv'),
        'context_menu': context_items,
    })
    context_items = []
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Update Streams', 'XBMC.RunPlugin(%s)' % (plugin.url_for(update_streams))))
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Set as IPTV File M3U', 'XBMC.RunPlugin(%s)' % (plugin.url_for(set_iptvsimple_m3u_file))))
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Remove id Rule', 'XBMC.RunPlugin(%s)' % (plugin.url_for(remove_m3u_id_rule))))
    items.append(
    {
        'label': "Streams",
        'path': plugin.url_for('streams'),
        'thumbnail':get_icon_path('tv'),
        'context_menu': context_items,
    })
    context_items = []
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add IPTV Simple Client EPG', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_iptvsimple_epg))))
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add EPG URL', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_epg_url))))
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add EPG File', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_epg_file))))
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Add Rytec EPG', 'XBMC.RunPlugin(%s)' % (plugin.url_for(add_rytec_epg))))
    items.append(
    {
        'label': "EPG Program Sources",
        'path': plugin.url_for('epg_sources'),
        'thumbnail':get_icon_path('tv'),
        'context_menu': context_items,
    })
    
    context_items = []
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Set Default Channels', 'XBMC.RunPlugin(%s)' % (plugin.url_for(default_channels)))) 
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Set Default Streams', 'XBMC.RunPlugin(%s)' % (plugin.url_for(default_streams))))        
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Clear', 'XBMC.RunPlugin(%s)' % (plugin.url_for(clear_channels))))
    items.append(
    {
        'label': "EPG Template",
        'path': plugin.url_for('epg_template'),
        'thumbnail':get_icon_path('tv'),
        'context_menu': context_items,
    })
    context_items = []
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Update Channels', 'XBMC.RunPlugin(%s)' % (plugin.url_for(update_channels))))
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Resolve Duplicates', 'XBMC.RunPlugin(%s)' % (plugin.url_for(duplicates))))
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Set as IPTV File EPG', 'XBMC.RunPlugin(%s)' % (plugin.url_for(set_iptvsimple_epg_file))))
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Disable IPTV Simple Client', 'XBMC.RunPlugin(%s)' % (plugin.url_for(disable_iptvsimple))))
    context_items.append(("[COLOR yellow][B]%s[/B][/COLOR] " % 'Enable IPTV Simple Client', 'XBMC.RunPlugin(%s)' % (plugin.url_for(enable_iptvsimple))))
    items.append(
    {
        'label': "EPG Channels",
        'path': plugin.url_for('channels'),
        'thumbnail':get_icon_path('tv'),
        'context_menu': context_items,
    })
    return items



if __name__ == '__main__':    
    plugin.run()
