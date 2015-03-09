# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import sys, random
import urllib, urllib2, cookielib
import re, base64
from watched import *
from array import *
from htmlentitydefs import name2codepoint as n2cp
import htmlentitydefs
# new since v0.95
import urlresolver
# new since 1.3.0
from player import bsPlayer

thisPlugin = int(sys.argv[1])
print thisPlugin

edenCompatibility = xbmcplugin.getSetting(thisPlugin,"caching")

if edenCompatibility=="true":
	useCaching=True
else:
	useCaching=False
	print "-- switched off caching for eden-compatibility"

addonInfo = xbmcaddon.Addon()
cacheFile = addonInfo.getAddonInfo('path')+"/cache.data"

urlHost = "http://www.burning-seri.es/"

# by Alphabet
regexContentA = "<ul id='serSeries'>(.*?)</ul>"
regexContentB = '<li><a href="(.*?)">(.*?)</a></li>'
regexContentC = '<div class="genre">.*?<span><strong>(.*?)</strong></span>.*?<ul>(.*?)</ul>.*?</div>'
regexSeasonsA = '<ul class="pages">.*?</ul>'
regexSeasonsB = '<li.*?><a href="(.*?)">([^<]+)</a></li>'
regexSeasonsPic = 'id="sp_right">.*?<img src="(.*?)" alt="[cC]+over"/>'
regexEpisodesA = '<table>.*?</table>'
regexEpisodesB = '(<td>([^<]+)</td>[\\n\s]+<td><a href="([^"]+)">[\\n\s]+(<strong>[^<]+</strong>)?[\\n\s]+(<span lang="en">[^<]+</span>)?[\\n\s]+</a></td>[\\n\s]+<td class="nowrap">[\\n\s]+<a class.*?</td>.*?</tr>)'
regexEpisodesC = '<strong>(.*?)</strong>'
regexEpisodesD = '<span lang="en">(.*?)</span>'
regexHostsA = 'Episode</h3>.*?<ul style="width: [0-9]{1,3}px;">(.*?)</ul>.*?</section>'
regexHostsB = '<a.*?href="(.*?)"><span.*?class="icon (.*?)"></span>(.*?)</a>'
regexShowA = '<div id="video_actions">.*?<div>.*?<a href="(.*?)" target="_blank"><span'
# ------------------------
# compile regexes on start
cRegConA = re.compile(regexContentA,re.DOTALL)
cRegConB = re.compile(regexContentB,re.DOTALL)
cRegConC = re.compile(regexContentC,re.DOTALL)
cRegSeaA = re.compile(regexSeasonsA,re.DOTALL)
cRegSeaB = re.compile(regexSeasonsB,re.DOTALL)
cRegSeaPic = re.compile(regexSeasonsPic,re.DOTALL)
cRegEpiA = re.compile(regexEpisodesA,re.DOTALL)
cRegEpiB = re.compile(regexEpisodesB,re.DOTALL)
cRegEpiC = re.compile(regexEpisodesC,re.DOTALL)
cRegEpiD = re.compile(regexEpisodesD,re.DOTALL)
cRegHosA = re.compile(regexHostsA,re.DOTALL)
cRegHosB = re.compile(regexHostsB,re.DOTALL)
cRegShoA = re.compile(regexShowA,re.DOTALL)

# ---------
# functions

def showContent(sortType):
	global thisPlugin
	print "[bs][showContent] started"
	seriesList = {}
	serie =[]
	picture = ""
	content = getUrl(urlHost+"serie-genre")
	if content:
		content = content.replace("&amp;","&")
		#print content
		matchC = cRegConC.findall(content)
		for n in matchC:
			#print n
			matchB = cRegConB.findall(n[1])
			for m in matchB:
				if sortType[0] == "G":
					serie = [n[0]+" : [B]"+m[1].strip()+"[/B]",m[0],picture]
					lKey = n[0]
				if sortType[0] == "A":
					serie = ["[B]"+m[1].strip()+"[/B] ("+n[0]+")",m[0],picture]
					helper = ord(m[1][0])
					if helper>90:
						helper = helper-32
					if (helper>64) and (helper<91):
						lKey = chr(helper).upper()
					else:
						lKey = "0"
				if lKey in seriesList:
					seriesList[lKey].append(serie)
				else:
					seriesList[lKey] = []
					seriesList[lKey].append(serie)
				
		if len(sortType)==1:
			addDirectoryItem(".sort by Alphabet", {"sortType": "A"})
			addDirectoryItem(".sort by Genre", {"sortType": "G"})
			addDirectoryItem("", {"sortType": "A"})
			for key in sorted(seriesList):
				skey = key
				if key =="0":
					skey = "0-9 etc"
				addDirectoryItem("[B]"+skey+"[/B] (%d)" % len(seriesList[key]), {"sortType": sortType+key})
		else:
			sKey = sortType[1:]
			for s in sorted(seriesList[sKey], key=lambda f:f[0]):
				if useCaching:
					cachedPic = readPictureData(s[1])
					if cachedPic:
						picture = cachedPic
						print "[bs][showContent] -- cached pic existing - "+picture
					else:
						print "[bs][showContent] -- pic not in cache"
						cPic = getUrl(urlHost+s[1])
						if cPic:
							cPic = cPic.replace("&amp;","&")
							matchPic = cRegSeaPic.findall(cPic)
							try:
								picture = "https:"+matchPic[0]
							except IndexError:
								picture = ""
							cachedPic = writePictureData(urllib.unquote(s[1]), picture)
				seriesName = unescape(s[0])
				# check if watched
				if readWatchedData(urlHost+s[1]):
					seriesName = changeToWatched(seriesName)
				addDirectoryItem(seriesName, {"urlS": s[1], "series":s[1],"doFav":"0"},picture)
	else:
		addDirectoryItem("Oops there was an url-error. network?", {"sortType": sortType})
	
	print "[bs][showContent] --- ok"	
	xbmcplugin.endOfDirectory(thisPlugin)

def showSeasons(urlS,series,doFav):
	global thisPlugin
	matchCover = ""
	print "[bs][showSeasons] started with "+urlS
	print "[bs][showSeasons]--- series Data"
	print series
	content = getUrl(urlS)
	matchA = cRegSeaA.findall(content)
	if matchA:
		matchB = cRegSeaB.findall(matchA[0])
		print "-- matchB"
		#print matchB
		if useCaching:
			matchCover = readPictureData(series)
			print "[bs][showSeasons] -- cached Picture - "+matchCover
		addDirectoryItem("[B]. "+series.replace("serie/","").replace("-"," ")+"[/B]", {},matchCover)
		seasonsWatched = 0
		for m in matchB:
			preString = ""
			if is_number(m[1]):
				preString = "Staffel "
			seasonName = unescape(preString+m[1])
			# check if watched
			if readWatchedData(urlHost+m[0]):
				seasonsWatched +=1
				seasonName = changeToWatched(seasonName)
			addDirectoryItem(seasonName, {"urlE": m[0], "series":series}, matchCover)
			#print m
		# mark series if all seasons were watched
		if seasonsWatched == len(matchB):
			markParentEntry(urlHost+series)
	else:
		addDirectoryItem("ERROR in Seasons matchA", {"urlS": urlS})
	print "[bs][showSeasons] --- ok"	
	xbmcplugin.endOfDirectory(thisPlugin)

def showEpisodes(urlE,series):
	global thisPlugin
	matchCover = ""
	print "[bs][showEpisodes] started with "+urlE
	content = getUrl(urlE)
	#print content
	print "[bs] --- series Data"
	print series
	matchA = cRegEpiA.findall(content)
	if useCaching:
		print "[bs][showEpisodes] -- reading cached picture - "+series
		matchCover = readPictureData(series)
		print "[bs][showEpisodes] cached Picture - "+matchCover
	print "[bs][showEpisodes] ---matchA"
	#print matchA
	if matchA:
		print "found matchA - now regexing"
		matchB = cRegEpiB.findall(matchA[0])
		print "matchB regexed"
		if matchB:
			#print "[bs][showEpisodes] ---matchB"
			episodesWatched = 0
			for m in matchB:
				matchD = cRegEpiD.findall(m[0])
				if matchD:
					englishTitle = " - "+matchD[0]
				else:
					englishTitle = ""
				mS = cRegEpiC.findall(m[0])
				#print mS
				if mS:
					print mS
					matchStrong = " - "+mS[0]
				else:
					matchStrong = ""
				episodeName = unescape(m[1].strip()+matchStrong+englishTitle)
				# check if watched
				if readWatchedData(urlHost+m[2]):
					episodesWatched += 1
					episodeName = changeToWatched(episodeName)
				addDirectoryItem(episodeName, {"urlH": m[2], "series":series, "urlE":urlE},matchCover)
			# if watched all episodes, mark Season
			if episodesWatched == len(matchB):
				markParentEntry(urlE)
		else:
			addDirectoryItem("ERROR in Episodes B regex - matchB", {"urlH": ""})
	else:
		addDirectoryItem("ERROR in Episodes A regex - matchA", {"urlH": ""})
	print "[bs][showEpisodes] ok"	
	xbmcplugin.endOfDirectory(thisPlugin)

def showHosts(urlH, series, urlE):
	global thisPlugin
	matchCover = ""
	print "[bs][showHosts] started with "+urlH
	if useCaching:
		matchCover = readPictureData(series)
		print "[bs][showHosts] cached Picture - "+matchCover
	content = getUrl(urlH)
	#print "-- showHosts"
	#print content
	matchA = cRegHosA.findall(content)
	print "[bs][showHosts] -- matchesA"
	print matchA
	matchB = cRegHosB.findall(matchA[0])
	print "[bs][showHosts] -- matchB"
	print matchB
	for m in matchB:
			#print m
			addDirectoryItem("Host: "+m[1].strip(), {"urlV": m[0],"urlE":urlE},matchCover)
			print "[bs][showHosts] -- "+m[1]+" : "+m[0]  
	print "[bs][showHosts] ok"	
	xbmcplugin.endOfDirectory(thisPlugin)
	
def showVideo(urlV,urlE):
	global thisPlugin
	print "[bs][showVideo] started on "+urlV
	print "[bs][showVideo] got urlE for watchedStatus: "+urlE
	content = getUrl(urlV)
	if content:
		#print content
		matchVideo = cRegShoA.findall(content)
		print "[bs][showVideo] matchVideo - "+matchVideo[0]
		videoLink = urlresolver.resolve(matchVideo[0]);
		print "[bs][showVideo] urlResolver returns - "
		print videoLink
		if videoLink:
			print "[bs][showVideo] urlResolver videoLink --"
			print videoLink
			#videoLink = unescape(videoLink)
			item = xbmcgui.ListItem(path=videoLink)
			bsPlayer().playStream(videoLink,urlV[:urlV.rfind("/")])
		else:
			addDirectoryItem("ERROR. Video deleted or urlResolver cant handle Host", {"urlV": "/"})
			xbmcplugin.endOfDirectory(thisPlugin)
	else:
		addDirectoryItem("ERROR. Video deleted or urlResolver cant handle Host", {"urlV": "/"})
		xbmcplugin.endOfDirectory(thisPlugin)
		
#def showFavorites():
#	global thisPlugin
#	print "[bs][showFavorites] started"
#	favs.add_my_fav_directory()

# -------- helper ------

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
	return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def getUrl(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		return response.read()
		response.close()
	except:
		return False

def addDirectoryItem(name, parameters={},pic=""):
	iconpic = pic
	if pic == "":
		iconpic = "DefaultFolder.png"
	li = xbmcgui.ListItem(name,iconImage=iconpic, thumbnailImage=pic)
	url = sys.argv[0] + '?' + urllib.urlencode(parameters)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)

def addPlayableItem(name, parameters={},pic=""):
	iconpic = pic
	if pic == "":
		iconpic = "DefaultFolder.png"
	li = xbmcgui.ListItem(name,iconImage=iconpic, thumbnailImage=pic)
	li.setProperty("IsPlayable","true")
	url = sys.argv[0] + '?' + urllib.urlencode(parameters)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=False)

	
def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, unicode(text, "UTF-8"), re.UNICODE)
	
# since v1.1.0
def writePictureData(id,url):
	global cacheFile
	f = xbmcvfs.File(cacheFile)
	d = f.read()
	f.close()
	f = xbmcvfs.File(cacheFile, 'w')
	b = d+id+"<>"+url+"\n"
	result = f.write(b)
	print "[bs][writePictureData] write -> "+ id + " <> " +url
	f.close()
	return result

def readPictureData(id):
	global cacheFile
	f = xbmcvfs.File(cacheFile)
	b = f.read()
	f.close()
	cacheData = b.splitlines()
	for n in cacheData:
		splittedData = n.split("<>")
		if splittedData[0]==id:
			print "[bs][readPictureData] found cached "+id
			return splittedData[1]
	return False


# ----- main -----
# ----------------
params = parameters_string_to_dict(sys.argv[2])
#showFavs = str(params.get("showFavs",""))
sortType = str(params.get("sortType", ""))
urlSeasons = str(params.get("urlS", ""))
doFav = str(params.get("doFav",""))
urlEpisodes = str(params.get("urlE", ""))
urlHosts = str(params.get("urlH", ""))
urlVideo = str(params.get("urlV", ""))
seriesName = str(params.get("sName", ""))
dataSeries = urllib.unquote(str(params.get("series", "")))

if not sys.argv[2]:
	# new start
	ok = showContent("A")
	
else:
	if sortType:
		ok = showContent(sortType)
#	if showFavs:
#		ok = showFavorites()
	if urlSeasons:
		newUrl = urlHost + urllib.unquote(urlSeasons)
		#print newUrl
		ok = showSeasons(newUrl,dataSeries, doFav)
	if urlEpisodes and not urlHosts and not urlVideo:
		newUrl = urlHost + urllib.unquote(urlEpisodes)
		#print newUrl
		ok = showEpisodes(newUrl,dataSeries)
	if urlHosts:
		newUrl = urlHost + urllib.unquote(urlHosts)
		#print newUrl
		ok = showHosts(newUrl,dataSeries,urlEpisodes)
	if urlVideo:
		newUrl = urlHost + urllib.unquote(urlVideo)
		#print newUrl
		ok = showVideo(newUrl,urlEpisodes)
