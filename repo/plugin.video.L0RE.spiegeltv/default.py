#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
	from urllib import quote, unquote, quote_plus, unquote_plus, urlencode  # Python 2.X
	from urllib2 import build_opener, HTTPCookieProcessor, Request, urlopen  # Python 2.X
	from cookielib import LWPCookieJar  # Python 2.X
	from urlparse import urljoin, urlparse, urlunparse  # Python 2.X
elif PY3:
	from urllib.parse import quote, unquote, quote_plus, unquote_plus, urlencode, urljoin, urlparse, urlunparse  # Python 3+
	from urllib.request import build_opener, HTTPCookieProcessor, Request, urlopen  # Python 3+
	from http.cookiejar import LWPCookieJar  # Python 3+
import json
import xbmcvfs
import shutil
import socket
import time
import io
import gzip
from bs4 import BeautifulSoup
import YDStreamExtractor


global debuging
pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addonPath = xbmc.translatePath(addon.getAddonInfo('path')).encode('utf-8').decode('utf-8')
dataPath    = xbmc.translatePath(addon.getAddonInfo('profile')).encode('utf-8').decode('utf-8')
temp           = xbmc.translatePath(os.path.join(dataPath, 'temp', '')).encode('utf-8').decode('utf-8')
defaultFanart = os.path.join(addonPath, 'fanart.jpg')
icon = os.path.join(addonPath, 'icon.png')
baseURL = "https://www.spiegel.tv"


if xbmcvfs.exists(temp) and os.path.isdir(temp):
	shutil.rmtree(temp, ignore_errors=True)
	xbmc.sleep(500)
xbmcvfs.mkdirs(temp)
cookie = os.path.join(temp, 'cookie.lwp')
cj = LWPCookieJar()

if xbmcvfs.exists(cookie):
	cj.load(cookie, ignore_discard=True, ignore_expires=True)

def py2_enc(s, encoding='utf-8'):
	if PY2 and isinstance(s, unicode):
		s = s.encode(encoding)
	return s

def py2_uni(s, encoding='utf-8'):
	if PY2 and isinstance(s, str):
		s = unicode(s, encoding)
	return s

def py3_dec(d, encoding='utf-8'):
	if PY3 and isinstance(d, bytes):
		d = d.decode(encoding)
	return d

def translation(id):
	LANGUAGE = addon.getLocalizedString(id)
	LANGUAGE = py2_enc(LANGUAGE)
	return LANGUAGE

def failing(content):
	log(content, xbmc.LOGERROR)

def debug(content):
	log(content, xbmc.LOGDEBUG)

def log(msg, level=xbmc.LOGNOTICE):
	msg = py2_enc(msg)
	xbmc.log("["+addon.getAddonInfo('id')+"-"+addon.getAddonInfo('version')+"]"+msg, level)

def getUrl(url, header=None):
	global cj
	opener = build_opener(HTTPCookieProcessor(cj))
	try:
		if header:
			opener.addheaders = header
		else:
			opener.addheaders =[('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0')]
			opener.addheaders = [('Accept-Encoding', 'gzip, deflate')]
		response = opener.open(url, timeout=30)
		if response.info().get('Content-Encoding') == 'gzip':
			content = py3_dec(gzip.GzipFile(fileobj=io.BytesIO(response.read())).read())
		else:
			content = py3_dec(response.read())
	except Exception as e:
		failure = str(e)
		if hasattr(e, 'code'):
			failing("(getUrl) ERROR - ERROR - ERROR : ########## {0} === {1} ##########".format(url, failure))
		elif hasattr(e, 'reason'):
			failing("(getUrl) ERROR - ERROR - ERROR : ########## {0} === {1} ##########".format(url, failure))
		content = ""
		return sys.exit(0)
	opener.close()
	try: cj.save(cookie, ignore_discard=True, ignore_expires=True)
	except: pass
	return content

def index():
	addDir('Popcorn - Zurücklehnen und Film schauen', baseURL+'/playlists/2543-popcorn-film-schauen-und-zuruecklehnen', 'listVideos', icon, sub='special')
	addDir('Sendungen', '0', 'listThemes', icon)
	addDir('Stöbern', '2', 'listThemes', icon)
	addDir('Studios', baseURL+'/allstudios', 'listStudios', icon)
	addDir('Meist gesehen', baseURL+'/hot', 'listVideos', icon, sub='normal')
	addDir('Neue Beiträge', baseURL+'/new', 'listVideos', icon, sub='normal')
	addDir('WEB-TV Playliste', baseURL+'/playlists/1395-webtv', 'listVideos', icon, sub='special')
	xbmcplugin.endOfDirectory(pluginhandle)

def listThemes(url):
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	content = getUrl(baseURL+'/start')
	selection = re.findall("data-target='categoriesholder{0}'><div id='catsholder{0}'>(.+?)</ul></div></div>".format(str(url)), content, re.DOTALL)
	for chtml in selection:
		part = chtml.split("class='underlinemagic'>")
		for i in range(1, len(part), 1):
			element = part[i]
			link = baseURL+re.compile("<a href='([^']+?)' data", re.DOTALL).findall(element)[0].strip()
			title = re.compile("data-navigateparam=.+?'>([^<]+?)</a>", re.DOTALL).findall(element)[0]
			title = py2_enc(title).strip()
			addDir(title, link, 'listVideos', icon, sub='special')
	xbmcplugin.endOfDirectory(pluginhandle)
  
def listStudios(url):
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	content = getUrl(url)
	htmlPage = BeautifulSoup(content, 'html.parser')  
	stud_block = htmlPage.find('div',attrs={'id':'rcblock'}) 
	Movies = stud_block.find_all('a',attrs={'data-navigateto':'withstudio'}) 
	for video in Movies:
		link = baseURL+video['href']
		image = video.find('img')['src']
		title = video.find('img')['alt']
		addDir(title, link, 'listVideos', image, sub='normal', serie=title)
	xbmcplugin.endOfDirectory(pluginhandle)  
  
def listVideos(url, sub, serie):
	content = getUrl(url)
	htmlPage = BeautifulSoup(content, 'html.parser')
	vid_block = htmlPage.find('div',attrs={'id':'rcblock'})
	if sub == 'special':
		Movies = vid_block.find_all('a',attrs={'class':'focusable tholder material'}) 
	else:
		Movies = vid_block.find_all('a',attrs={'class':'focusable vholder material fortwolines'})
	for video in Movies:
		link = baseURL+video['href']
		image = video.find('img')['src']
		tagline = video.find('div',attrs={'class':'autocut bold cardsubtitle'}).get_text()
		plot = "[B][COLOR FF76EE00]"+tagline+"[/COLOR][/B][CR]"
		if sub == 'special':
			title = video.find('div',attrs={'class':'autocut bold cardtitle'}).get_text()
			plot += video.find('div',attrs={'class':'tdesc'}).get_text()
			matchD = video.find('div',attrs={'class':'tholderbottom'}).get_text()
		else:
			title = video.find('div',attrs={'class':'twolines bold cardtitle'}).get_text()
			matchD = video.find('div',attrs={'class':'autocut addinfo'}).get_text()
		duration = re.compile('([0-9]+)', re.DOTALL).findall(matchD)[0]    
		duration = int(duration)*60
		addLink(title, link, 'playVideo', image, duration, plot, tagline, serie)
	xbmcplugin.endOfDirectory(pluginhandle)  

def playVideo(url):    
	vid = YDStreamExtractor.getVideoInfo(url, quality=2) # quality is 0=SD, 1=720p, 2=1080p and is a maximum
	stream_url = vid.streamURL() # This is what Kodi (XBMC) will play
	stream_url = stream_url.split('|')[0]
	xbmcplugin.setResolvedUrl(pluginhandle, True, xbmcgui.ListItem(path=stream_url))

def parameters_string_to_dict(parameters):
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split('&')
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict

def addDir(name, url, mode, iconimage, plot=None, sub=None, serie=None):   
	u = sys.argv[0]+"?url="+quote_plus(url)+"&mode="+str(mode)+"&sub="+str(sub)+"&serie="+str(serie)
	liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels={'TvShowtitle': serie, 'Title': name, 'Plot': plot})
	liz.setArt({'poster': iconimage, 'fanart': defaultFanart})
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

def addLink(name, url, mode, iconimage, duration=None, plot=None, tagline=None, serie=None):
	u = sys.argv[0]+"?url="+quote_plus(url)+"&mode="+str(mode)
	liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels={'TvShowtitle': serie, 'Title': name, 'Plot': plot, 'Duration': duration, 'Tagline': tagline, 'Studio': 'Spiegel.tv', 'mediatype': 'video'})
	liz.setArt({'poster': iconimage, 'fanart': defaultFanart, 'landscape': iconimage})
	liz.addStreamInfo('Video', {'Duration': duration})
	liz.setProperty('IsPlayable', 'true')
	liz.setContentLookup(False)
	xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)

params = parameters_string_to_dict(sys.argv[2])
url = unquote_plus(params.get('url', ''))
mode = unquote_plus(params.get('mode', ''))
sub= unquote_plus(params.get('sub', ''))
serie= unquote_plus(params.get('serie', ''))

if mode == 'listThemes':
	listThemes(url)  
elif mode == 'listStudios':
	listStudios(url)
elif mode == 'listVideos':
	listVideos(url, sub, serie)
elif mode == 'playVideo':
	playVideo(url)
else:
	index()