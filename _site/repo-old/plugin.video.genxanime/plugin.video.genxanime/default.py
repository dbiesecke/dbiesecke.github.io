#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib,re,os
import xbmcplugin,xbmcgui
import xbmcaddon,xbmc

dialog = xbmcgui.Dialog()
try: import requests
except: dialog.ok("FEHLER", "Bitte script.module.requests installieren")

pluginhandle = int(sys.argv[1])

addon = xbmcaddon.Addon(id='plugin.video.genxanime')
home = addon.getAddonInfo('path').decode('utf-8')
image = xbmc.translatePath(os.path.join(home, 'icon.png'))
datapath = xbmc.translatePath('special://profile/addon_data/plugin.video.genxanime/')
favs = os.path.join(datapath,'favs.txt')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:27.0) Gecko/20100101 Firefox/27.0', 'Host':'www.genx-anime.org'}
api_url = 'https://www.burning-seri.es/api/'
Sgerman = addon.getSetting('german')

if not os.path.isdir(datapath):
  os.mkdir(datapath)

def kategorien():
        addDir('Neu','/index.php','liste','','','','')
	addDir('Laufende Serien', 'http://www.genx-anime.org/ajax/calendar_show.inc.php','laufende','','','','')
        addDir('Serien','http://www.genx-anime.org/index.php?do=display&type=tv','abc','','','','')
        addDir('Movies','http://www.genx-anime.org/index.php?do=display&type=movie','abc','','','','')
        addDir('OVAs und Specials','http://www.genx-anime.org/index.php?do=display&type=OVA+%26+Specials','abc','','','','')
        addDir('Top 100','/index.php?do=toplist','liste','','','','')
        addDir('Genres','http://genx-anime.org/index.php?do=suche','genres','','','','')
        addDir('Suche','http://www.genx-anime.org/index.php?do=display&q=','suche','','','','')
        addDir('Meine Anime','','meine','','','','')
        xbmcplugin.endOfDirectory(pluginhandle)
		
def genres():
	url = params['url']
        content = requests.get(url, headers=headers).content
	gens = re.findall('filter\[genre\].*?value="(.+?)"', content)
	for genre in gens:
	  url = 'http://www.genx-anime.org/index.php?do=display&genre=' + genre
          addDir(genre,url,'liste','','','','')
        xbmcplugin.endOfDirectory(pluginhandle)

def suche():
	url = params['url']
	kb = xbmc.Keyboard('', 'Suche', False)
	kb.doModal()
	search_entered = kb.getText().replace(' ','+')
	url = url + search_entered
	content = requests.get(url, headers=headers).content
	if '<h2>Animes</h2>' in content:
	  liste(url)
	else:
	  name = re.findall('<h4>\n(.*?)<br/>', content)[0]
	  id = re.findall("id: '(.*?)'", content)[0]
	  cover = re.findall('<img alt=.*?src="(.*?)"', content)[0]
	  cover = 'http://www.genx-anime.org/' + cover
	  url = 'id=' + id
	  addDir(name,url,'folgen',cover,'','','')
	  xbmcplugin.endOfDirectory(pluginhandle)

def meine():
	if os.path.exists(favs):
	  fh = open(favs, 'r')
	  content = fh.read()
	  match = re.findall('{"name":"(.*?)","url":"(.*?)","cover":"(.*?)","plot":"(.*?)"}', content, re.DOTALL)
	  for name,url,cover,plot in match:
	    cm = []
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('rem')+"&iconimage="+urllib.quote_plus(cover)+"&plot="+urllib.quote_plus(plot)
	    cm.append( ('von Meine Anime entfernen', "XBMC.RunPlugin(%s)" % u) )
	    if api_url in url:
	      addDir(name,url,'staffeln',cover,plot,'','',cm=cm)
	    else:
	      addDir(name,url,'folgen',cover,plot,'','',cm=cm)
	  fh.close()
        xbmcplugin.endOfDirectory(pluginhandle)

def add():
	name = urllib.unquote_plus(params['name'])
	url = urllib.unquote_plus(params['url'])
	try: cover = urllib.unquote_plus(params['iconimage'])
	except: cover = ''
	try: plot = urllib.unquote_plus(params['plot'])
	except:
	  if api_url in url:
	    json = requests.get(url+str(1)).json()
	    seasons = json['series']['seasons']
	    try: plot = json['series']['description'].encode('UTF-8')
	    except: plot = ''
	  else:
	    ajax_url = 'http://www.genx-anime.org/ajax/calendar_details.inc.php'
	    aid = url.split('id=')[-1]
	    data = {'aid': str(aid)}
	    json = requests.post(ajax_url, headers=headers, data=data).json()
	    plot = json['beschreibung'].encode('utf-8')
	amventry = '{"name":"'+name+'","url":"'+url+'","cover":"'+cover+'","plot":"'+plot+'"}'
	if os.path.exists(favs):
	  fh = open(favs, 'r')
	  content = fh.read()
	  fh.close()
	  if content.find(amventry) == -1:
	    fh = open(favs, 'a')
	    fh.write(amventry+"\n")
	    fh.close()
	else:
	  fh = open(favs, 'a')
	  fh.write(amventry+"\n")
	  fh.close()
	dialog.ok("INFO", "Anime zu 'Meine Anime' hinzugefuegt")

def rem():
	name = urllib.unquote_plus(params['name'])
	url = urllib.unquote_plus(params['url'])
	cover = urllib.unquote_plus(params['iconimage'])
	plot = urllib.unquote_plus(params['plot'])
	amventry = '{"name":"'+name+'","url":"'+url+'","cover":"'+cover+'","plot":"'+plot+'"}'
	fh = open(favs, 'r')
	content = fh.read()
	fh.close()
	entry = content[content.find(amventry):]
	fh = open(favs, 'w')
	fh.write(content.replace(amventry+"\n", ""))
	fh.close()
	dialog.ok("INFO", "Anime von 'Meine Anime' entfernt")

def laufende():
	url = params['url']
	data = {'offset': '0', 'limit': '100', 'status': '0'}
	content = requests.post(url, headers=headers, data=data).content
	serie = re.findall('data-aid="(.*?)" class="calendar_name">(.*?)</a>', content)
	for aid, name in serie:
	  if not aid == '0':
	    cover = 'http://www.genx-anime.org/upload/cover/180px/' + str(aid) + '.png'
	    url = 'http://www.genx-anime.org/index.php?do=display&id=' + str(aid)
	    plot = ''
	    cm = []
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('add')+"&iconimage="+urllib.quote_plus(cover)+"&plot="+urllib.quote_plus(plot)
	    cm.append( ('zu Meine Anime hinzufuegen', "XBMC.RunPlugin(%s)" % u) )
	    addDir(name,url,'folgen',cover,plot,'','',cm=cm)
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(pluginhandle)

def abc():
        addDir('Burning Serien','https://www.burning-seri.es/api/series:genre','genre_serien','','','','')
	url = params['url']
        content = requests.get(url, headers=headers).content
        match=re.findall('<li><a href="(.*?)">(.*?)</a></li>', content)
        for url,name in match:
          mainurl='http://www.genx-anime.org/'
          if 'display' in url:
            url = mainurl + url
            addDir(name,url,'liste','','','','')
        xbmcplugin.endOfDirectory(pluginhandle)

def liste(url=False):
	if not url: url = params['url']
	try:
          content = requests.get(url, headers=headers).content
          match = re.findall('<dt style=.*?</dt>', content, re.DOTALL)[0]
	  match = re.findall('href="(.*?)"', match)
	except:
	  match = [url]
	for url in match:
          url = 'http://www.genx-anime.org/' + url
	  content = requests.get(url, headers=headers).content
	  items = re.findall('<li class="item">.*?</li>', content, re.DOTALL)
	  for item in items:
	    url = re.findall('<a href="(.*?)">', item)[0]
            url = 'http://www.genx-anime.org/' + url
	    name = re.findall('title="(.*?)\|', item)[0]
            name = name.replace("|","")
	    cover = re.findall('<img class=.*? src=.*?/.*?/.*?/(.*?)>', item)[0]
            cover = cover.replace("'","")
            cover = 'http://www.genx-anime.org/upload/cover/180px/' + cover
	    genre = re.findall('Genre</strong>: (.*?)<br/>', item)[0]
	    try: setting = re.findall('Setting</strong>: (.*?)<br/>', item)[0]
	    except: setting = ''
	    plot = re.findall('<br/><br/>(.*?)</span>', item, re.DOTALL)[0]
            plot = plot.replace("&quot;","'")
	    year = re.findall('<dt class="ayear">(.*?)</dt>', item, re.DOTALL)[0]
	    episodes = re.findall('<dt class="aepisode">(.*?)</dt>', item, re.DOTALL)[0]
            episodes = episodes.replace(" ","").replace("\n","")
	    languages = re.findall('<img title="(.*?)"', item)
	    languages = ', '.join(languages).replace('Enth\xc3\xa4lt ','')
	    if not 'de' in languages and Sgerman == 'true':
	      pass
	    else:
	      plot = 'Setting: ' + setting + '\n' + 'Episoden: ' + episodes + ' Sprache(n): ' + languages + '\n' + plot
	      cm = []
	      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('add')+"&iconimage="+urllib.quote_plus(cover)+"&plot="+urllib.quote_plus(plot)
	      cm.append( ('zu Meine Anime hinzufuegen', "XBMC.RunPlugin(%s)" % u) )
              addDir(name,url,'folgen',cover,plot,genre,year,cm=cm)
        xbmcplugin.endOfDirectory(pluginhandle)

def folgen():
	url = params['url']
	ajax_url = 'http://www.genx-anime.org/ajax/calendar_details.inc.php'
	aid = url.split('id=')[-1]
	data = {'aid': str(aid)}
	json = requests.post(ajax_url, headers=headers, data=data).json()
	folgen = json['folgen']
	for folge in folgen:
	  name = ''
	  name = folgen[folge]['name'].encode('utf-8')
	  name = 'E0' + str(folge) + '.' + name
	  streams = folgen[folge]['Stream']
	  links = []
	  linksde = []
	  linksen = []
	  for stream in streams:
	    link = stream['link']
	    dub = stream['dub']
	    sub = stream['sub']
	    if 'de' in dub:
	      linksde.append(link)
	    elif 'en' in sub:
	      linksen.append(link)
	    else:
	      links.append(link)
	  if linksde:
	    addLink(name,'','resolver','',linksde)
	  elif not linksde and linksen and Sgerman == 'false':
	    addLink(name,'','resolver','',linksen)
	  elif not linksde and linksen and Sgerman == 'true':
	    pass
	  else:
	    addLink(name,'','resolver','',links)
          xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(pluginhandle)

def resolver(links=False):
	if not links: links = params['links']
	try:
	  stream = ''
	  if links:
	    try:
	      import ast
	      links = ast.literal_eval(links)	
	      links = [n.strip() for n in links]
	    except: pass
	    host1 = [i for i in links if addon.getSetting('host1') in i]
	    host2 = [i for i in links if addon.getSetting('host2') in i]
	    host3 = [i for i in links if addon.getSetting('host3') in i]
	    host4 = [i for i in links if addon.getSetting('host4') in i]
	    host5 = [i for i in links if addon.getSetting('host5') in i]
	    host6 = [i for i in links if addon.getSetting('host6') in i]
	    hoster_list = [host1,host2,host3,host4,host5,host6]
	    print hoster_list
	    for hoster in hoster_list:
	      print hoster
	      for link in hoster:
	        import resolver
	        if 'vidzi' in link and not stream:
	          stream = resolver.resolvers().vidzi(link)
	        elif 'streamcloud' in link and not stream:
	          stream = resolver.resolvers().streamcloud(link)
	        elif 'vivo' in link and not stream:
	          stream = resolver.resolvers().vivo(link)
	        elif 'shared' in link and not stream:
	          stream = resolver.resolvers().shared(link)
	        elif 'novamov' in link and not stream:
	          stream = resolver.resolvers().novamov(link)
	        elif 'primeshare' in link and not stream:
	          stream = resolver.resolvers().primeshare(link)
	    if stream:
              listitem = xbmcgui.ListItem(path=stream)
              xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	    else:
	      dialog.ok("INFO", "Alle Streams Offline")
	  else:
	    dialog.ok("INFO", "Keine Links Vorhanden")
	except:
	  dialog.ok("FEHLER", "Resolver Fehlgeschlagen")

# start burning-seri.es

def genre_serien():
	url = params['url']
	genre = 'Anime'
	genres = requests.get(url).json()
	series = genres[genre]['series']
	for serie in series:
	  name = serie['name'].encode('UTF-8')
	  id = serie['id']
	  url = api_url + 'series/' + str(id) + '/'
	  cm = []
	  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('add')
	  cm.append( ('zu Meine Anime hinzufuegen', "XBMC.RunPlugin(%s)" % u) )
	  addDir(name,url,'staffeln','','','','',cm=cm)
	xbmcplugin.endOfDirectory(pluginhandle)

def staffeln():
	serien_url = params['url']
	a = 1
	season_url = serien_url + str(a)
	json = requests.get(season_url).json()
	seasons = json['series']['seasons']
	try: plot = json['series']['description'].encode('UTF-8')
	except: plot = ''
	try: genre = json['series']['data']['genre'][0]
	except: genre = ''
	try: year = json['series']['start']
	except: year = ''
	if seasons == '1':
	  episoden(season_url)
	else:
	  while a <= int(seasons):
	    addDir('Staffel ' + str(a),serien_url + str(a),'episoden','',plot,genre,year)
	    a += 1
	xbmcplugin.endOfDirectory(pluginhandle)

def episoden(url=False):
	if not url: season_url = params['url']
	else: season_url = url
	episodes = requests.get(season_url).json()
	episodes = episodes['epi']
	for episode in episodes:
	  epi = episode['epi']
	  titlede = episode['german']
	  titleen = episode['english']
          if titlede:
	    name = 'E0' + epi + '.' + titlede
	  elif titleen:
	    name = 'E0' + epi + '.' + titleen
	  else:
	    name = 'E0' + epi
	  name = name.encode('UTF-8')
	  addLink(name,season_url + '/' + epi,'streams','')
	xbmcplugin.endOfDirectory(pluginhandle)

def streams():
	episoden_url = params['url']
	ids = []
	links = requests.get(episoden_url).json()
	links = links['links']
	for link in links:
	  id = link['id']
	  hoster = link['hoster']
	  if hoster == 'Streamcloud' or hoster == 'Vidzi' or hoster == 'Vivo' or hoster == 'Shared' or hoster == 'Novamov' or hoster == 'Primeshare':
	    ids.append(id)
	if ids:
	  resolverb(ids)
	else:
	  dialog.ok("INFO", "Keine Links Vorhanden")

def resolverb(ids=False):
	links = []
	for id in ids:
	  watch_url = api_url + 'watch/' + id
	  url = requests.get(watch_url).json()
	  url = url['fullurl']
	  links.append(url)
	resolver(links)

# ende burning-seri.es

def addLink(name,url,mode,iconimage,links=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&links="+str(links)
        item=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        item.setInfo( type="Video", infoLabels={ "Title": name } )
        item.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item)

def addDir(name,url,mode,iconimage,plot,genre,year,cm=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        item=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        item.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Genre": genre, "Year": year } )
        if cm:
          item.addContextMenuItems( cm )
        xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item,isFolder=True)

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
	  params=sys.argv[2]
	  cleanedparams=params.replace('?','')
	  if (params[len(params)-1]=='/'):
	    params=params[0:len(params)-2]
	  pairsofparams=cleanedparams.split('&')
	  param={}
	  for i in range(len(pairsofparams)):
	    splitparams={}
	    splitparams=pairsofparams[i].split('=')
	    if (len(splitparams))==2:
	      param[splitparams[0]]=urllib.unquote_plus(splitparams[1])
	return param

params=get_params()
try:
    mode=params["mode"]
except:
    mode=None
print "Mode: "+str(mode)
print "Parameters: "+str(params)

if mode==None:
    kategorien()
else:
    exec '%s()' % mode
