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
from datetime import datetime, timedelta
import io
import gzip


global debuging
pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addonPath = xbmc.translatePath(addon.getAddonInfo('path')).encode('utf-8').decode('utf-8')
dataPath = xbmc.translatePath(addon.getAddonInfo('profile')).encode('utf-8').decode('utf-8')
temp        = xbmc.translatePath(os.path.join(dataPath, 'temp', '')).encode('utf-8').decode('utf-8')
channelFavsFile = os.path.join(dataPath, 'my_DMAX_favourites.txt').encode('utf-8').decode('utf-8')
defaultFanart = os.path.join(addonPath, 'fanart.jpg')
icon = os.path.join(addonPath, 'icon.png')
spPIC = os.path.join(addonPath, 'resources', 'media', '').encode('utf-8').decode('utf-8')
useThumbAsFanart = addon.getSetting("useThumbAsFanart") == "true"
enableAdjustment = addon.getSetting("show_settings") == "true"
enableInputstream = addon.getSetting("inputstream") == "true"
enableLibrary = addon.getSetting("dmax_library") == "true"
mediaPath = addon.getSetting("mediapath")
updatestd = addon.getSetting("updatestd")
baseURL = "https://www.dmax.de/"

xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')

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

def getUrl(url, header=None, agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'):
	global cj
	opener = build_opener(HTTPCookieProcessor(cj))
	opener.addheaders = [('User-Agent', agent), ('Accept-Encoding', 'gzip, deflate')]
	try:
		if header: opener.addheaders = header
		response = opener.open(url, timeout=30)
		if response.info().get('Content-Encoding') == 'gzip':
			content = py3_dec(gzip.GzipFile(fileobj=io.BytesIO(response.read())).read())
		else:
			content = py3_dec(response.read())
	except Exception as e:
		failure = str(e)
		failing("(getUrl) ERROR - ERROR - ERROR : ########## {0} === {1} ##########".format(url, failure))
		content = ""
		return sys.exit(0)
	opener.close()
	try: cj.save(cookie, ignore_discard=True, ignore_expires=True)
	except: pass
	return content

def ADDON_operate(TESTING):
	js_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.GetAddonDetails", "params": {"addonid":"'+TESTING+'", "properties": ["enabled"]}, "id":1}')
	if '"enabled":false' in js_query:
		try:
			xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.SetAddonEnabled", "params": {"addonid":"'+TESTING+'", "enabled":true}, "id":1}')
			failing("(ADDON_operate) ERROR - ERROR - ERROR :\n##### Das benötigte Addon : *"+TESTING+"* ist NICHT aktiviert !!! #####\n##### Es wird jetzt versucht die Aktivierung durchzuführen !!! #####")
		except: pass
	if '"error":' in js_query:
		xbmcgui.Dialog().ok(addon.getAddonInfo('id'), translation(30501).format(TESTING))
		failing("(ADDON_operate) ERROR - ERROR - ERROR :\n##### Das benötigte Addon : *"+TESTING+"* ist NICHT installiert !!! #####")
		return False
	if '"enabled":true' in js_query:
		return True

def index():
	addDir(translation(30601), "", "listShowsFavs", icon)
	addDir(translation(30602), baseURL+"api/search?query=*&limit=50", "listseries", icon, nosub="overview_all")
	addDir(translation(30603), "", "listthemes", icon)
	addDir(translation(30604), baseURL+"api/shows/highlights?limit=50", "listseries", icon, nosub="featured")
	addDir(translation(30605), baseURL+"api/shows/neu?limit=50", "listseries", icon, nosub="recently_added")
	addDir(translation(30606), baseURL+"api/shows/beliebt?limit=50", "listseries", icon, nosub="most_popular")
	if enableAdjustment:
		addDir(translation(30607), "", "aSettings", icon)
		if enableInputstream:
			if ADDON_operate('inputstream.adaptive'):
				addDir(translation(30608), "", "iSettings", icon)
			else:
				addon.setSetting("inputstream", "false")
	xbmcplugin.endOfDirectory(pluginhandle)

def listthemes():
	debug("-------------------------- LISTTHEMES --------------------------")
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
	html = getUrl(baseURL+"themen")
	content = html[html.find('href="/themen">Themen</a><div class="header__nav__dd-wrapper">')+1:]
	content = content[:content.find('</ul></div>')]
	result = re.compile('<a href="(.*?)">(.*?)</a>').findall(content)
	for link, name in result:
		url = baseURL+"api/genres/"+link.split('/')[-1]+"?limit=100"
		name = py2_enc(name).replace('&amp;', '&').strip()
		debug("(listthemes) ### NAME : "+str(name)+" || LINK : "+str(link)+" || URL : "+str(url)+" ###")
		if "themen" in link:
			addDir(name, url, "listseries", icon, nosub="overview_themes")
	xbmcplugin.endOfDirectory(pluginhandle)

def listseries(url, PAGE, POS, ADDITION):
	debug("-------------------------- LISTSERIES --------------------------")
	debug("(listseries) ### URL : "+str(url)+" ### PAGE : "+str(PAGE)+" ### POS : "+str(POS)+" ### ADDITION : "+str(ADDITION)+" ###")
	count = int(POS)
	readyURL = url+"&page="+str(PAGE)
	content = getUrl(readyURL)
	debug("(listseries) ##### CONTENT : "+str(content)+" #####")
	DATA = json.loads(content)
	if "search?query" in url:
		elements = DATA['shows']
	else:
		elements = DATA['items']
	for elem in elements:
		debug("(listseries) ##### ELEMENT : "+str(elem)+" #####")
		title = py2_enc(elem['title']).strip()
		name = title
		idd = ""
		if 'id' in elem and elem['id'] != "" and elem['id'] != None:
			idd = elem['id']
		plot = ""
		if 'description' in elem and elem['description'] != "" and elem['description'] != None:
			plot = py2_enc(elem['description']).replace('\n\n\n', '\n\n').strip()
		image = ""
		if 'image' in elem and 'src' in elem['image'] and elem['image']['src'] != "" and elem['image']['src'] != None:
			image = elem['image']['src']
		debug("(listseries) noFilter ### NAME : "+ str(name) +" || IDD : "+ str(idd) +" || IMAGE : "+ str(image) +" ###")
		if idd !="" and len(idd) < 9 and plot != "" and image != "":
			count += 1
			if 'beliebt' in url:
				name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			try: 
				if elem['hasNewEpisodes']: name = name+translation(30609)
			except: pass
			debug("(listseries) Filtered ### NAME : "+str(name)+" || IDD : "+str(idd)+" || IMAGE : "+str(image)+" ###")
			addType=1
			if os.path.exists(channelFavsFile):
				with open(channelFavsFile, 'r') as output:
					lines = output.readlines()
					for line in lines:
						idd_FS = re.compile('URL=<uu>(.*?)</uu>').findall(line)[0]
						if idd == idd_FS: addType=2
			addDir(name, idd, "listepisodes", image, plot, nosub=ADDITION, originalSERIE=title, addType=addType)
	currentRESULT = count
	debug("(listseries) ##### currentRESULT : "+str(currentRESULT)+" #####")
	try:
		currentPG = DATA['meta']['currentPage']
		totalPG = DATA['meta']['totalPages']
		debug("(listseries) ##### currentPG : "+str(currentPG)+" from totalPG : "+str(totalPG)+" #####")
		if int(currentPG) < int(totalPG):
			addDir(translation(30610), url, "listseries", spPIC+"nextpage.png", page=int(currentPG)+1, position=int(currentRESULT), nosub=ADDITION)
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)

def listepisodes(idd, originalSERIE):
	debug("-------------------------- LISTEPISODES --------------------------")
	COMBI = []
	SELECT = []
	pos1 = 0
	url = baseURL+"api/show-detail/"+str(idd)
	debug("(listepisodes) ### URL : "+str(url)+" ### originalSERIE : "+str(originalSERIE)+" ###")
	try:
		content = getUrl(url)
		debug("(listepisodes) ##### CONTENT : "+str(content)+" #####")
		DATA = json.loads(content)
	except: return xbmcgui.Dialog().notification(translation(30521).format(str(idd)), translation(30522), icon, 12000)
	genstr = ""
	genreList=[]
	if 'show' in DATA and 'genres' in DATA['show'] and DATA['show']['genres'] != "" and DATA['show']['genres'] != None:
		for item in DATA['show']['genres']:
			gNames = py2_enc(item['name'])
			genreList.append(gNames)
		genstr =' / '.join(genreList)
	if 'episode' in DATA['videos'] or 'standalone' in DATA['videos']:
		if 'episode' in DATA['videos']:
			subelement = DATA['videos']['episode']
			if PY2: makeITEMS = subelement.iteritems # for (key, value) in subelement.iteritems():  # Python 2x
			elif PY3: makeITEMS = subelement.items # for (key, value) in subelement.items():  # Python 3+
			for number,videos in makeITEMS():
				for vid in videos:
					if 'isPlayable' in vid and vid['isPlayable'] == True:
						debug("(listepisodes) ##### subelement-1-vid : "+str(vid)+" #####")
						season = ""
						if 'season' in vid and vid['season'] != "" and str(vid['season']) != "0" and vid['season'] != None:
							season = str(vid['season']).zfill(2)
						episode = ""
						if 'episode' in vid and vid['episode'] != "" and str(vid['episode']) != "0" and vid['episode'] != None:
							episode = str(vid['episode']).zfill(2)
						title = py2_enc(vid['name']).strip()
						if season != "" and episode != "":
							title1 = '[COLOR chartreuse]S'+season+'E'+episode+':[/COLOR]'
							title2 = title
							number = 'S'+season+'E'+episode
						else:
							title1 = title
							title2 = ""
							number = ""
						begins = None
						year = None
						startTIMES = None
						endTIMES = None
						Note_1 = ""
						Note_2 = ""
						Note_3 = ""
						if 'publishStart' in vid and vid['publishStart'] != "" and vid['publishStart'] != None and not str(vid['publishStart']).startswith('1970'):
							try:
								startDATES = datetime(*(time.strptime(vid['publishStart'], '%Y-%m-%dT%H:%M:%SZ')[0:6])) # 2019-06-23T14:10:00Z
								LOCALstart = utc_to_local(startDATES)
								startTIMES = LOCALstart.strftime('%d.%m.%y • %H:%M')
								begins =  LOCALstart.strftime('%d.%m.%Y')
							except: pass
						if 'publishEnd' in vid and vid['publishEnd'] != "" and vid['publishEnd'] != None and not str(vid['publishEnd']).startswith('1970'):
							try:
								endDATES = datetime(*(time.strptime(vid['publishEnd'], '%Y-%m-%dT%H:%M:%SZ')[0:6])) # 2019-06-23T14:10:00Z
								LOCALend = utc_to_local(endDATES)
								endTIMES = LOCALend.strftime('%d.%m.%y • %H:%M')
							except: pass
						if 'airDate' in vid and vid['airDate'] != "" and vid['airDate'] != None and not str(vid['airDate']).startswith('1970'):
							year = vid['airDate'][:4]
						if startTIMES: Note_1 = translation(30611).format(str(startTIMES))
						if endTIMES: Note_2 = translation(30612).format(str(endTIMES))
						if 'description' in vid and vid['description'] != "" and vid['description'] != None:
							Note_3 = py2_enc(vid['description']).replace('\n\n\n', '\n\n').strip()
						plot = Note_1+Note_2+Note_3
						image = ""
						if 'image' in vid and 'src' in vid['image'] and vid['image']['src'] != "" and vid['image']['src'] != None:
							image = vid['image']['src']
						idd2 = ""
						if 'id' in vid and vid['id'] != "" and vid['id'] != None:
							idd2 = vid['id']
						else: continue
						duration = int(vid['videoDuration']/1000)
						COMBI.append([number, title1, title2, idd2, image, plot, duration, season, episode, genstr, year, begins])
		if 'standalone' in DATA['videos']:
			subelement = DATA['videos']['standalone']
			for item in subelement:
				if 'isPlayable' in item and item['isPlayable'] == True:
					debug("(listepisodes) ##### subelement-2-item : "+str(item)+" #####")
					season = "00"
					if 'season' in item and item['season'] != "" and str(item['season']) != "0" and item['season'] != None:
						season = str(item['season']).zfill(2)
					episode = ""
					if 'episode' in item and item['episode'] != "" and str(item['episode']) != "0" and item['episode'] != None:
						episode = str(item['episode']).zfill(2)
					title = py2_enc(item['name']).strip()
					begins = None
					year = None
					airdate = None
					startTIMES = None
					endTIMES = None
					Note_1 = ""
					Note_2 = ""
					Note_3 = ""
					if 'publishStart' in item and item['publishStart'] != "" and item['publishStart'] != None and not str(item['publishStart']).startswith('1970'):
						try:
							startDATES = datetime(*(time.strptime(item['publishStart'], '%Y-%m-%dT%H:%M:%SZ')[0:6])) # 2019-06-23T14:10:00Z
							LOCALstart = utc_to_local(startDATES)
							startTIMES = LOCALstart.strftime('%d.%m.%y • %H:%M')
							begins =  LOCALstart.strftime('%d.%m.%Y')
						except: pass
					if 'publishEnd' in item and item['publishEnd'] != "" and item['publishEnd'] != None and not str(item['publishEnd']).startswith('1970'):
						try:
							endDATES = datetime(*(time.strptime(item['publishEnd'], '%Y-%m-%dT%H:%M:%SZ')[0:6])) # 2019-06-23T14:10:00Z
							LOCALend = utc_to_local(endDATES)
							endTIMES = LOCALend.strftime('%d.%m.%y • %H:%M')
						except: pass
					if 'airDate' in item and item['airDate'] != "" and item['airDate'] != None and not str(item['airDate']).startswith('1970'):
						year = item['airDate'][:4]
						airdate = item['airDate'][:10]
					if startTIMES: Note_1 = translation(30611).format(str(startTIMES))
					if endTIMES: Note_2 = translation(30612).format(str(endTIMES))
					if 'description' in item and item['description'] != "" and item['description'] != None:
						Note_3 = py2_enc(item['description']).replace('\n\n\n', '\n\n').strip()
					plot = Note_1+Note_2+Note_3
					image = ""
					if 'image' in item and 'src' in item['image'] and item['image']['src'] != "" and item['image']['src'] != None:
						image = item['image']['src']
					idd2 = ""
					if 'id' in item and item['id'] != "" and item['id'] != None:
						idd2 = item['id']
					else: continue
					duration = int(item['videoDuration']/1000)
					SELECT.append([title, idd2, image, plot, duration, season, episode, genstr, year, airdate, begins])
			if SELECT:
				for title, idd2, image, plot, duration, season, episode, genstr, year, airdate, begins in sorted(SELECT, key=lambda ad:ad[9], reverse=False):
					pos1 += 1
					if season != "00" and episode != "":
						title1 = '[COLOR orangered]S'+season+'E'+episode+':[/COLOR]'
						title2 = title
						number = 'S'+season+'E'+episode
					else:
						episode = str(pos1).zfill(2)
						title1 = '[COLOR orangered]S00E'+episode+':[/COLOR]'
						title2 = title+'  (Special)'
						number = 'S00E'+episode
					COMBI.append([number, title1, title2, idd2, image, plot, duration, season, episode, genstr, year, begins])
	else:
		debug("(listepisodes) ##### Keine COMBINATION-List - Kein Eintrag gefunden #####")
		return xbmcgui.Dialog().notification(translation(30523), translation(30524).format(originalSERIE), icon, 8000)
	if COMBI:
		if addon.getSetting("sorting") == "1":
			xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
			xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
			xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DURATION)
		else:
			COMBI = sorted(COMBI, key=lambda b:b[0], reverse=True)
		for number, title1, title2, idd2, image, plot, duration, season, episode, genstr, year, begins in COMBI:
			if addon.getSetting("sorting") == "1" and begins:
				xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
			name = title1.strip()+"  "+title2.strip()
			if title2 == "":
				name = title1.strip()
			debug("(listepisodes) ### NAME : "+str(name)+" || IDD : "+str(idd2)+" || GENRE : "+str(genstr)+" ###")
			debug("(listepisodes) ### IMAGE : "+str(image)+" || SEASON : "+str(season)+" || EPISODE : "+str(episode)+" ###")
			addLink(name, idd2, "playvideo", image, plot, duration, seriesname=originalSERIE, season=season, episode=episode, genre=genstr, year=year, begins=begins)
	xbmcplugin.endOfDirectory(pluginhandle)

def playvideo(idd2):
	debug("-------------------------- PLAYVIDEO --------------------------")
	content = getUrl(baseURL)
	for cookief in cj:
		debug("(playvideo) ##### COOKIE : "+str(cookief)+" #####")
		if "sonicToken" in str(cookief):
			key = re.compile('sonicToken=(.*?) for', re.DOTALL).findall(str(cookief))[0]
			break
	playurl = "https://sonic-eu1-prod.disco-api.com/playback/videoPlaybackInfo/"+str(idd2)
	header = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'), ('Authorization', 'Bearer '+key)]
	result = getUrl(playurl, header=header)
	debug("(playvideo) ##### RESULT : "+str(result)+" #####")
	DATA = json.loads(result)
	videoURL = DATA['data']['attributes']['streaming']['hls']['url']
	log("(playvideo) StreamURL : "+videoURL)
	listitem = xbmcgui.ListItem(path=videoURL)
	listitem.setProperty('IsPlayable', 'true')
	if enableInputstream:
		if ADDON_operate('inputstream.adaptive'):
			licfile = DATA['data']['attributes']['protection']['schemes']['clearkey']['licenseUrl']
			debug("(playvideo) ##### LIC-FILE : "+str(licfile)+" #####")
			licurl = getUrl(licfile, header=header)
			lickey = re.compile('"kid":"(.*?)"', re.DOTALL).findall(licurl)[0]
			debug("(playvideo) ##### LIC-KEY : "+str(lickey)+" #####")
			listitem.setProperty('inputstreamaddon', 'inputstream.adaptive')
			listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
			listitem.setProperty('inputstream.adaptive.license_key', lickey)
			listitem.setContentLookup(False)
		else:
			addon.setSetting("inputstream", "false")
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def listShowsFavs():
	debug("-------------------------- LISTSHOWSFAVS --------------------------")
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
	if os.path.exists(channelFavsFile):
		with open(channelFavsFile, 'r') as textobj:
			lines = textobj.readlines()
			for line in lines:
				name = re.compile('TITLE=<tt>(.*?)</tt>').findall(line)[0]
				url = re.compile('URL=<uu>(.*?)</uu>').findall(line)[0]
				thumb = re.compile('THUMB=<ii>(.*?)</ii>').findall(line)[0]
				plot = re.compile('PLOT=<pp>(.*?)</pp>').findall(line)[0].replace('#n#', '\n')
				debug("(listShowsFavs) ##### NAME : "+str(name)+" | URL : "+str(url)+" #####")
				addDir(name, url, "listepisodes", thumb, plot, originalSERIE=name, FAVdel=True)
	xbmcplugin.endOfDirectory(pluginhandle)

def favs(param):
	mode = param[param.find('MODE=')+9:+12]
	SERIES_entry = param[param.find('###TITLE='):]
	SERIES_entry = SERIES_entry[:SERIES_entry.find('END###')]
	name = re.compile('TITLE=<tt>(.*?)</tt>').findall(SERIES_entry)[0]
	url = re.compile('URL=<uu>(.*?)</uu>').findall(SERIES_entry)[0]
	if mode == "ADD":
		if os.path.exists(channelFavsFile):
			with open(channelFavsFile, 'a+') as textobj:
				content = textobj.read()
				if content.find(SERIES_entry) == -1:
					textobj.seek(0,2) # change is here (for Windows-Error = "IOError: [Errno 0] Error") - because Windows don't like switching between reading and writing at same time !!!
					textobj.write(SERIES_entry+'END###\n')
		else:
			with open(channelFavsFile, 'a') as textobj:
				textobj.write(SERIES_entry+'END###\n')
		xbmc.sleep(500)
		xbmcgui.Dialog().notification(translation(30525), translation(30526).format(name), icon, 8000)
	elif mode == "DEL":
		with open(channelFavsFile, 'r') as output:
			lines = output.readlines()
		with open(channelFavsFile, 'w') as input:
			for line in lines:
				if url not in line:
					input.write(line)
		xbmc.executebuiltin('Container.Refresh')
		xbmc.sleep(1000)
		xbmcgui.Dialog().notification(translation(30525), translation(30527).format(name), icon, 8000)

def utc_to_local(dt):
	if time.localtime().tm_isdst: return dt - timedelta(seconds=time.altzone)
	else: return dt - timedelta(seconds=time.timezone)

def tolibrary(param):
	log("-------------------------- TOLIBRARY --------------------------")
	if mediaPath =="":
		xbmcgui.Dialog().ok(addon.getAddonInfo('id'), translation(30502))
	elif mediaPath !="" and ADDON_operate('service.L0RE.cron'):
		LIB_entry = param[param.find('###START'):]
		LIB_entry = LIB_entry[:LIB_entry.find('END###')]
		url = LIB_entry.split('###')[2]
		name = LIB_entry.split('###')[3]
		stunden = LIB_entry.split('###')[4]
		newURL = 'plugin://{0}/?mode=generatefiles&url={1}&name={2}'.format(addon.getAddonInfo('id'), url, name.replace('&', '%26'))
		newURL = quote_plus(newURL)
		source = quote_plus(mediaPath+fixPathSymbols(name))
		log("(tolibrary) ##### newURL : "+str(newURL)+" #####")
		log("(tolibrary) ##### SOURCE : "+str(source)+" #####")
		xbmc.executebuiltin('RunPlugin(plugin://service.L0RE.cron/?mode=adddata&name={0}&stunden={1}&url={2}&source={3})'.format(name.replace('&', '%26'), stunden, newURL, source))
		xbmcgui.Dialog().notification(translation(30528), translation(30529).format(name,str(stunden)), icon, 12000)

def generatefiles(idd, show):
	debug("-------------------------- GENERATEFILES --------------------------")
	if not enableLibrary or mediaPath =="":
		return
	COMBINATION = []
	SELECTION = []
	pos2 = 0
	SPECIALS = False
	url = baseURL+"api/show-detail/"+str(idd)
	debug("(generatefiles) ##### URL : "+str(url)+" #####")
	ppath =py2_uni(mediaPath)+py2_uni(fixPathSymbols(show))
	debug("(generatefiles) ##### PPATH : "+str(ppath)+" #####")
	if os.path.isdir(ppath):
		shutil.rmtree(ppath, ignore_errors=True)
		xbmc.sleep(500)
	os.mkdir(ppath)
	try:
		content = getUrl(url)
		DATA = json.loads(content)
		TVS_title = py2_enc(DATA['show']['name'])
	except:
		return
	genreList=[]
	if 'show' in DATA and 'genres' in DATA['show'] and DATA['show']['genres'] != "" and DATA['show']['genres'] != None:
		for item in DATA['show']['genres']:
			gNames = py2_enc(item['name'])
			genreList.append(gNames)
	try: EP_genre1 = genreList[0]
	except: EP_genre1 = ""
	try: EP_genre2 = genreList[1]
	except: EP_genre2 = ""
	try: EP_genre3 = genreList[2]
	except: EP_genre3 = ""
	if 'episode' in DATA['videos'] or 'standalone' in DATA['videos']:
		if not 'episode' in DATA['videos']:
			SPECIALS = True
		if 'episode' in DATA['videos']:
			subelement = DATA['videos']['episode']
			if PY2: makeITEMS = subelement.iteritems
			elif PY3: makeITEMS = subelement.items
			for number,videos in makeITEMS():
				for vid in videos:
					if 'isPlayable' in vid and vid['isPlayable'] == True:
						debug("(generatefiles) ##### subelement-1-vid : "+str(vid)+" #####")
						EP_season = ""
						if 'season' in vid and vid['season'] != "" and str(vid['season']) != "0" and vid['season'] != None:
							EP_season = str(vid['season']).zfill(2)
						EP_episode = ""
						if 'episode' in vid and vid['episode'] != "" and str(vid['episode']) != "0" and vid['episode'] != None:
							EP_episode = str(vid['episode']).zfill(2)
						EP_title = py2_enc(vid['name']).strip()
						if EP_season != "" and EP_episode != "":
							EP_title = 'S'+EP_season+'E'+EP_episode+': '+EP_title
						startTIMES = None
						endTIMES = None
						Note_1 = ""
						Note_2 = ""
						Note_3 = ""
						if 'publishStart' in vid and vid['publishStart'] != "" and vid['publishStart'] != None and not str(vid['publishStart']).startswith('1970'):
							try:
								startDATES = datetime(*(time.strptime(vid['publishStart'], '%Y-%m-%dT%H:%M:%SZ')[0:6])) # 2019-06-23T14:10:00Z
								LOCALstart = utc_to_local(startDATES)
								startTIMES = LOCALstart.strftime('%d.%m.%y • %H:%M')
							except: pass
						if 'publishEnd' in vid and vid['publishEnd'] != "" and vid['publishEnd'] != None and not str(vid['publishEnd']).startswith('1970'):
							try:
								endDATES = datetime(*(time.strptime(vid['publishEnd'], '%Y-%m-%dT%H:%M:%SZ')[0:6])) # 2019-06-23T14:10:00Z
								LOCALend = utc_to_local(endDATES)
								endTIMES = LOCALend.strftime('%d.%m.%y • %H:%M')
							except: pass
						if startTIMES: Note_1 = translation(30611).format(str(startTIMES))
						if endTIMES: Note_2 = translation(30612).format(str(endTIMES))
						if 'description' in vid and vid['description'] != "" and vid['description'] != None:
							Note_3 = py2_enc(vid['description']).replace('\n\n\n', '\n\n').strip()
						EP_plot = Note_1+Note_2+Note_3
						EP_image = ""
						if 'image' in vid and 'src' in vid['image'] and vid['image']['src'] != "" and vid['image']['src'] != None:
							EP_image = vid['image']['src']
						EP_idd = ""
						if 'id' in vid and vid['id'] != "" and vid['id'] != None:
							EP_idd = vid['id']
						else: continue
						Add_HO = 0
						Add_SE = 0
						MILLIS = int(vid['videoDuration'])
						HOURS = (MILLIS/(1000*60*60))%24
						if HOURS >= 1:
							Add_HO = HOURS*60
						MINS = (MILLIS/(1000*60))%60
						SECS = (MILLIS/1000)%60
						if SECS >= 30:
							Add_SE = 1
						EP_duration = MINS+Add_HO+Add_SE
						try: EP_airdate = vid['airDate'][:10]
						except: EP_airdate = vid['publishStart'][:10]
						try: EP_yeardate = vid['airDate'][:4]
						except: EP_yeardate = vid['publishStart'][:4]
						episodeFILE = py2_uni(fixPathSymbols(EP_title))
						COMBINATION.append([episodeFILE, EP_title, TVS_title, EP_idd, EP_season, EP_episode, EP_plot, EP_duration, EP_image, EP_genre1, EP_genre2, EP_genre3, EP_yeardate, EP_airdate])
		if 'standalone' in DATA['videos']:
			subelement = DATA['videos']['standalone']
			for item in subelement:
				if 'isPlayable' in item and item['isPlayable'] == True:
					debug("(generatefiles) ##### subelement-2-item : "+str(item)+" #####")
					EP_season = "00"
					if 'season' in item and item['season'] != "" and str(item['season']) != "0" and item['season'] != None:
						EP_season = str(item['season']).zfill(2)
					EP_episode = ""
					if 'episode' in item and item['episode'] != "" and str(item['episode']) != "0" and item['episode'] != None:
						EP_episode = str(item['episode']).zfill(2)
					EP_title2 = py2_enc(item['name']).strip()
					startTIMES = None
					endTIMES = None
					Note_1 = ""
					Note_2 = ""
					Note_3 = ""
					if 'publishStart' in item and item['publishStart'] != "" and item['publishStart'] != None and not str(item['publishStart']).startswith('1970'):
						try:
							startDATES = datetime(*(time.strptime(item['publishStart'], '%Y-%m-%dT%H:%M:%SZ')[0:6])) # 2019-06-23T14:10:00Z
							LOCALstart = utc_to_local(startDATES)
							startTIMES = LOCALstart.strftime('%d.%m.%y • %H:%M')
						except: pass
					if 'publishEnd' in item and item['publishEnd'] != "" and item['publishEnd'] != None and not str(item['publishEnd']).startswith('1970'):
						try:
							endDATES = datetime(*(time.strptime(item['publishEnd'], '%Y-%m-%dT%H:%M:%SZ')[0:6])) # 2019-06-23T14:10:00Z
							LOCALend = utc_to_local(endDATES)
							endTIMES = LOCALend.strftime('%d.%m.%y • %H:%M')
						except: pass
					if startTIMES: Note_1 = translation(30611).format(str(startTIMES))
					if endTIMES: Note_2 = translation(30612).format(str(endTIMES))
					if 'description' in item and item['description'] != "" and item['description'] != None:
						Note_3 = py2_enc(item['description']).replace('\n\n\n', '\n\n').strip()
					EP_plot = Note_1+Note_2+Note_3
					EP_image = ""
					if 'image' in item and 'src' in item['image'] and item['image']['src'] != "" and item['image']['src'] != None:
						EP_image = item['image']['src']
					EP_idd = ""
					if 'id' in item and item['id'] != "" and item['id'] != None:
						EP_idd = item['id']
					else: continue
					Add_HO = 0
					Add_SE = 0
					MILLIS = int(item['videoDuration'])
					HOURS = (MILLIS/(1000*60*60))%24
					if HOURS >= 1:
						Add_HO = HOURS*60
					MINS = (MILLIS/(1000*60))%60
					SECS = (MILLIS/1000)%60
					if SECS >= 30:
						Add_SE = 1
					EP_duration = MINS+Add_HO+Add_SE
					try: EP_airdate = item['airDate'][:10]
					except: EP_airdate = item['publishStart'][:10]
					try: EP_yeardate = item['airDate'][:4]
					except: EP_yeardate = item['publishStart'][:4]
					SELECTION.append([EP_title2, TVS_title, EP_idd, EP_season, EP_episode, EP_plot, EP_duration, EP_image, EP_genre1, EP_genre2, EP_genre3, EP_yeardate, EP_airdate])
			if SELECTION:
				for EP_title2, TVS_title, EP_idd, EP_season, EP_episode, EP_plot, EP_duration, EP_image, EP_genre1, EP_genre2, EP_genre3, EP_yeardate, EP_airdate in sorted(SELECTION, key=lambda Ea:Ea[12], reverse=False):
					pos2 += 1
					if EP_season != "00" and EP_episode != "":
						EP_title = 'S'+EP_season+'E'+EP_episode+': '+EP_title2
					else:
						EP_episode = str(pos2).zfill(2)
						EP_title = 'S00E'+EP_episode+': '+EP_title2
					episodeFILE = py2_uni(fixPathSymbols(EP_title))
					COMBINATION.append([episodeFILE, EP_title, TVS_title, EP_idd, EP_season, EP_episode, EP_plot, EP_duration, EP_image, EP_genre1, EP_genre2, EP_genre3, EP_yeardate, EP_airdate])
	else:
		return
	for episodeFILE, EP_title, TVS_title, EP_idd, EP_season, EP_episode, EP_plot, EP_duration, EP_image, EP_genre1, EP_genre2, EP_genre3, EP_yeardate, EP_airdate in COMBINATION:
		nfo_EPISODE_string = os.path.join(ppath, episodeFILE+".nfo")
		with open(nfo_EPISODE_string, 'a') as textobj:
			textobj.write(
'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<episodedetails>
    <title>{0}</title>
    <showtitle>{1}</showtitle>
    <season>{2}</season>
    <episode>{3}</episode>
    <plot>{4}</plot>
    <runtime>{5}</runtime>
    <thumb>{6}</thumb>
    <genre clear="true">{7}</genre>
    <genre>{8}</genre>
    <genre>{9}</genre>
    <year>{10}</year>
    <aired>{11}</aired>
    <studio clear="true">DMAX</studio>
</episodedetails>'''.format(EP_title, TVS_title, EP_season, EP_episode, EP_plot, EP_duration, EP_image, EP_genre1, EP_genre2, EP_genre3, EP_yeardate, EP_airdate))
		streamfile = os.path.join(ppath, episodeFILE+".strm")
		debug("(generatefiles) ##### streamfile : "+py2_enc(streamfile)+" #####")
		file = xbmcvfs.File(streamfile, 'w')
		file.write('plugin://'+addon.getAddonInfo('id')+'/?mode=playvideo&url='+str(EP_idd))
		file.close()
	TVS_season = str(DATA['show']['seasonNumbers'])
	TVS_episode = str(DATA['show']['episodeCount'])
	if SPECIALS and SELECTION:
		TVS_season = "00"
		TVS_episode = str(pos2).zfill(2)
	TVS_plot = py2_enc(DATA['show']['description']).replace('\n\n\n', '\n\n')
	TVS_image = DATA['show']['image']['src']
	try: TVS_airdate = DATA['videos']['latestVideo']['airDate'][:10]
	except: TVS_airdate = DATA['videos']['latestVideo']['publishStart'][:10]
	try: TVS_yeardate = DATA['videos']['latestVideo']['airDate'][:4]
	except: TVS_yeardate = DATA['videos']['latestVideo']['publishStart'][:4]
	nfo_SERIE_string = os.path.join(ppath,"tvshow.nfo")
	with open(nfo_SERIE_string, 'a') as textobj:
		textobj.write(
'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<tvshow>
    <title>{0}</title>
    <showtitle>{0}</showtitle>
    <season>{1}</season>
    <episode>{2}</episode>
    <plot>{3}</plot>
    <thumb aspect="landscape" type="" season="">{4}</thumb>
    <fanart url="">
        <thumb dim="1280x720" colors="" preview="{4}">{4}</thumb>
    </fanart>
    <genre clear="true">{5}</genre>
    <genre>{6}</genre>
    <genre>{7}</genre>
    <year>{8}</year>
    <aired>{9}</aired>
    <studio clear="true">DMAX</studio>
</tvshow>'''.format(TVS_title, TVS_season, TVS_episode, TVS_plot, TVS_image, EP_genre1, EP_genre2, EP_genre3, TVS_yeardate, TVS_airdate))
	xbmcplugin.endOfDirectory(pluginhandle) 

def fixPathSymbols(structure): # Sonderzeichen für Pfadangaben entfernen
	structure = structure.strip()
	structure = structure.replace(' ', '_')
	structure = re.sub('[{@$%#^\\/;,:*?!\"+<>|}]', '_', structure)
	structure = structure.replace('______', '_').replace('_____', '_').replace('____', '_').replace('___', '_').replace('__', '_')
	if structure.startswith('_'):
		structure = structure[structure.rfind('_')+1:]
	if structure.endswith('_'):
		structure = structure[:structure.rfind('_')]
	return structure

def parameters_string_to_dict(parameters):
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split('&')
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict

def addDir(name, url, mode, image, plot=None, page=1, position=0, nosub=0, originalSERIE="", addType=0, FAVdel=False):
	u = sys.argv[0]+'?url='+quote_plus(url)+'&page='+str(page)+'&position='+str(position)+'&nosub='+str(nosub)+'&originalSERIE='+quote_plus(originalSERIE)+'&mode='+str(mode)
	liz = xbmcgui.ListItem(name)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': plot})
	liz.setArt({'icon': icon, 'thumb': image, 'poster': image, 'fanart': defaultFanart})
	if useThumbAsFanart and image != icon:
		liz.setArt({'fanart': image})
	entries = []
	if addType == 1 or addType == 2:
		if addType == 1 and FAVdel == False:
			playListInfos_1 = 'MODE=<mm>ADD</mm> ###TITLE=<tt>{0}</tt> URL=<uu>{1}</uu> THUMB=<ii>{2}</ii> PLOT=<pp>{3}</pp> END###'.format(originalSERIE, url, image, plot.replace('\n', '#n#'))
			entries.append([translation(30651), 'RunPlugin('+sys.argv[0]+'?mode=favs&url='+quote_plus(playListInfos_1)+')'])
		if enableLibrary:
			libListInfos = '###START###{0}###{1}###{2}###END###'.format(url, originalSERIE, updatestd)
			debug("(addDir) ##### libListInfos : "+py2_enc(libListInfos)+" #####")
			entries.append([translation(30653), 'RunPlugin('+sys.argv[0]+'?mode=tolibrary&url='+quote_plus(libListInfos)+')'])
	if FAVdel == True:
		playListInfos_2 = 'MODE=<mm>DEL</mm> ###TITLE=<tt>{0}</tt> URL=<uu>{1}</uu> THUMB=<ii>{2}</ii> PLOT=<pp>{3}</pp> END###'.format(name, url, image, plot)
		entries.append([translation(30652), 'RunPlugin('+sys.argv[0]+'?mode=favs&url='+quote_plus(playListInfos_2)+')'])
	liz.addContextMenuItems(entries, replaceItems=False)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

def addLink(name, url, mode, image, plot=None, duration=None, seriesname=None, season=None, episode=None, genre=None, year=None, begins=None):
	u = sys.argv[0]+'?url='+quote_plus(url)+'&mode='+str(mode)
	liz = xbmcgui.ListItem(name)
	ilabels = {}
	ilabels['Season'] = season
	ilabels['Episode'] = episode
	ilabels['Tvshowtitle'] = seriesname
	ilabels['Title'] = name
	ilabels['Tagline'] = None
	ilabels['Plot'] = plot
	ilabels['Duration'] = duration
	if begins != None:
		ilabels['Date'] = begins
	ilabels['Year'] = year
	ilabels['Genre'] = genre
	ilabels['Director'] = None
	ilabels['Writer'] = None
	ilabels['Studio'] = 'DMAX'
	ilabels['Mpaa'] = None
	ilabels['Mediatype'] = 'episode'
	liz.setInfo(type='Video', infoLabels=ilabels)
	liz.setArt({'icon': icon, 'thumb': image, 'poster': image, 'fanart': defaultFanart})
	if useThumbAsFanart and image != icon:
		liz.setArt({'fanart': image})
	liz.addStreamInfo('Video', {'Duration': duration})
	liz.setProperty('IsPlayable', 'true')
	liz.setContentLookup(False)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)

params = parameters_string_to_dict(sys.argv[2])
name = unquote_plus(params.get('name', ''))
url = unquote_plus(params.get('url', ''))
mode = unquote_plus(params.get('mode', ''))
image = unquote_plus(params.get('image', ''))
page = unquote_plus(params.get('page', ''))
position = unquote_plus(params.get('position', ''))
nosub = unquote_plus(params.get('nosub', ''))
originalSERIE = unquote_plus(params.get('originalSERIE', ''))
stunden = unquote_plus(params.get('stunden', ''))

if mode == 'aSettings':
	addon.openSettings()
elif mode == 'iSettings':
	xbmcaddon.Addon('inputstream.adaptive').openSettings()
elif mode == 'listthemes':
	listthemes()  
elif mode == 'listseries':
	listseries(url, page, position, nosub)
elif mode == 'listepisodes':
	listepisodes(url, originalSERIE)
elif mode == 'playvideo':
	playvideo(url)
elif mode == 'listShowsFavs':
	listShowsFavs()
elif mode == 'favs':
	favs(url)
elif mode == 'tolibrary':
	tolibrary(url)
elif mode == 'generatefiles':
	generatefiles(url, name)
else:
	index()