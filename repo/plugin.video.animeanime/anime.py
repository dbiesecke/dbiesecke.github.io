# -*- coding: utf-8 -*-

import sys, time
import urllib,os
import xbmc,xbmcplugin,xbmcgui
import urlparse, json
import threading

from resources.lib import mal
from resources.lib import common
from resources.lib.sites import burning
from resources.lib.sites import genx
from resources.lib.sites import tavernakoma
from resources.lib.sites import world24
from resources.lib.sites import tube
from resources.lib.sites import amvnews
from resources.lib.sites import anisearch

pluginhandle = int(sys.argv[1])
addon = common.get_addon()
image = common.get_image()
_clear_cache = addon.getSetting('clear_cache') == 'true'
load_info = addon.getSetting('load_info')
prefer_ihosts = addon.getSetting('prefer_ihosts') == 'true'
viewShows = addon.getSetting('viewShows') == 'true'
forceView = addon.getSetting('forceView') == 'true'
view = addon.getSetting('view')
views = { 'Liste': '50', 'Grosse Liste': '51', 'Vorschaubild': '500', 'Poster': '501', 
            'Fanart': '508', 'Medieninformationen': '504', 'Medieninformationen 2': '503', 'Medieninformationen 3': '515', 'Breit': '505' }
if view: 
    viewId = views[view]

_sites = [(genx, addon.getSetting('genx')), (burning, addon.getSetting('burning')), (tube, addon.getSetting('tube')), (world24, addon.getSetting('world24')), (tavernakoma, addon.getSetting('tavernakoma')), (anisearch, addon.getSetting('anisearch'))]
sites = [i[0] for i in _sites if i[1] == 'true']
_mirror_sites = [(world24, addon.getSetting('world24')), (tavernakoma, addon.getSetting('tavernakoma')), (tube, addon.getSetting('tube')), (anisearch, addon.getSetting('anisearch'))]
mirror_sites = [i[0] for i in _mirror_sites if i[1] == 'true']
    
def root():
    addDir('Neu','index.php','get_anime_list','')
    addDir('Airing Anime', 'calendar_show.inc.php','list_airing_anime','')
    addDir('Serien','index.php?do=display&type=tv','list_alphabet','')
    addDir('Movies','index.php?do=display&type=movie','list_alphabet','')
    addDir('OVAs und Specials','index.php?do=display&type=OVA+%26+Specials','list_alphabet','')
    addDir('Genres','','list_genres','')
    addDir('Top 100','index.php?do=toplist','get_anime_list','')
    addDir('AMV TV','','play_amv','')
    addDir('Suche','','list_search','')
    addDir('Meine Anime','','list_my_anime','')
    if _clear_cache: addDir('Clear Cache','','clear_cache','')
    xbmcplugin.endOfDirectory(pluginhandle)

def list_my_anime():
    my_anime_list = []
    entries = mal.get_my_anime_entries()
    if entries:
        for entry in entries:
            for site in _sites:
                if entry['site'] in str(site[0]):
                    id = entry['id']
                    anime = site[0].get_anime_info(id)
                    my_anime_list.append(anime)
        list_anime(my_anime_list)

def add_to_mal():
    id = args['url'][0]
    site = args['site'][0]
    try: mal.add_to_mal(site,id)
    except: pass

def remove_from_mal():
    id = args['url'][0]
    site = args['site'][0]
    try: mal.remove_from_mal(site,id)
    except: pass
    
def list_airing_anime():
    url = args['url'][0]
    aids = genx.get_airing_anime_aids(url)
    if aids:
        anime_list = genx.get_anime_list(aids)
        list_anime(anime_list)

def show_similar():
    name = args['name'][0]
    anime_list = anisearch.get_similar(name)
    anime_list = common.remove_duplicates(anime_list)
    for anime in anime_list:
        cover = anime['cover']
        name = anime['original'].encode('utf-8')
        addDir(name,'','list_search',cover)
    xbmcplugin.endOfDirectory(pluginhandle)
        
def list_search():
    name = args['name'][0]
    if name == 'Suche': name = False
    aids = genx.get_search_aids(name)
    if aids:
        anime_list = genx.get_anime_list(aids)
        list_anime(anime_list)

def list_genres():
    genres = genx.get_genres()
    for genre in genres:
        url = 'index.php?do=display&genre=%s' % genre
        addDir(genre,url,'get_anime_list','')
    xbmcplugin.endOfDirectory(pluginhandle)

def list_alphabet():
    type_url = args['url'][0]
    alphabet = genx.get_alphabet()
    for abc in alphabet:
        url = type_url + '&char=' + abc
        addDir(abc,url,'get_anime_list','')
    xbmcplugin.endOfDirectory(pluginhandle)
    
def get_anime_list():
    url = args['url'][0]
    if '&type=tv&char=' in url:
        abc = args['name'][0]
        anime_list = abc_threads(url,abc)
    elif 'index.php' == url:
        anime_list = get_new_list(url)
    else: anime_list = genx.get_anime_list(url)
    if anime_list: list_anime(anime_list)

def get_new_list(url):
    anime_list = []
    for site in sites:
        if 'genx' in str(site):
            anime_list = genx.get_anime_list(url)
        else:
            new_list = site.get_new_series()
            for anime in new_list:
                if anime and load_info == 'true':
                    id = anime['id']
                    anime_info = site.get_anime_info(id)
                    if anime_info: anime = anime_info
                anime_list.insert(0, anime)
    return anime_list
    
def abc_threads(url, abc):
    anime_list = []
    threads = []
    for site in sites: threads.append(threading.Thread(target=get_abc_list, args=(site,anime_list,url,abc)))
    [i.start() for i in threads]
    [i.join() for i in threads]
    anime_list = common.remove_duplicates(anime_list)
    return anime_list
    
def get_abc_list(site,anime_list,url,abc):
    if site == genx:
        abc_list = genx.get_anime_list(url)
        for anime in abc_list:
            anime_list.append(anime)
    else:
        abc_list = site.get_abc_series(abc)
        for anime in abc_list:
            if anime and load_info == 'true':
                if not anime['beschreibung']:
                    id = anime['id']
                    anime_info = site.get_anime_info(id)
                    if anime_info: anime = anime_info
            anime_list.append(anime)
    return anime_list
    
def list_anime(anime_list):
    for anime in anime_list:
        if anime:
            try:
                aid = anime['id']
                name = anime['original']
                try: name = name.encode('utf-8')
                except: name = name
                try: 
                    plot = anime['beschreibung']
                    try: plot = plot.encode('utf-8')
                    except: plot = plot
                except: plot = ''
                try: episodes = anime['folgenzahl']
                except: episodes = 0
                try: 
                    final_genres = ''
                    genres = anime['genre']
                    for genre in genres:
                        try: genre = genre.encode('utf-8')
                        except: genre = genre
                        final_genres += genre+' '
                except: genre = ''
                try: episodes_aired = anime['length']
                except: episodes_aired = 0
                try: 
                    setting = anime['setting']
                    try: setting = setting.encode('utf-8')
                    except: setting = setting
                except: setting = ''
                try: typ = anime['typ']
                except: typ = ''
                try: year = anime['year']
                except: year = ''
                #try: languages = anime['languages']
                #except: languages = 'de'
                try: site = anime['site']
                except: site = 'genx'
                try: cover = anime['cover']
                except: 
                    if site == 'genx': cover = 'http://www.genx-anime.org/upload/cover/180px/%s.png' % str(aid)
                    else: cover = ''
                cm = []
                if args['name'][0] == 'Meine Anime':
                    u=sys.argv[0]+"?url="+urllib.quote_plus(str(aid))+"&mode="+urllib.quote_plus('remove_from_mal')+"&site="+urllib.quote_plus(str(site))
                    cm.append( ('Delete %s' % name, "XBMC.RunPlugin(%s)" % u) )
                else:
                    u=sys.argv[0]+"?url="+urllib.quote_plus(str(aid))+"&mode="+urllib.quote_plus('add_to_mal')+"&site="+urllib.quote_plus(str(site))
                    cm.append( ('Add %s' % name, "XBMC.RunPlugin(%s)" % u) )
                addAnime(site,name,aid,'list_episodes',cover,plot,final_genres,year,episodes,episodes_aired,cm)
            except:
                pass
    if not args['name'][0] == 'Neu' and not args['name'][0] == 'Top 100':
        xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_STUDIO)
        xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    if viewShows:
        xbmcplugin.setContent(pluginhandle, 'tvshows')
    xbmcplugin.endOfDirectory(pluginhandle)
    xbmc.sleep(100)
    xbmc.executebuiltin('Container.SetViewMode('+viewId+')')

def list_episodes():
    site = args['site'][0]
    id = args['url'][0]
    name = args['name'][0]
    anime = name
    cover = args['iconimage'][0]
    episodes = ''
    if site == 'burning':
        list_burning_seasons(id, cover)
    else:
        if _sites[1][1] == 'true':
            burning_seasons = burning.get_burning_seasons(name)
            for season in burning_seasons:
                name = season['name'].encode('utf-8')
                bid = season['id']
                cover = season['cover']
                addDir(name,bid,'list_burning_episodes',cover)
        episodes = eval(site).get_episodes(id)
        if episodes:
            if site == 'genx':
                for episode in episodes:
                    try: name = episodes[episode]['name'].encode('utf-8')
                    except: name = ''
                    #name = 'Folge %s: %s' % (str(episode), name)
                    name = '%s .E0%s. %s' % (anime,str(episode), name)
                    addEpisode(site,name,id,'get_mirrors',anime,episode)
            else:
                for epi in episodes:
                    try: name = epi['name'].encode('utf-8')
                    except: name = epi['name']
                    url = epi['url']
                    episode = epi['episode'] 
                    addEpisode(site,anime+' -.'+name,url,'get_mirrors',anime,episode)
        xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(pluginhandle)
    
def list_burning_seasons(id, cover):
    seasons = burning.get_seasons(id)
    for i in range(int(seasons)):
        name = 'S0%s' % str(i+1)
        new_id = '%s/%s/' % (str(id), str(i+1))
        addDir(name,new_id,'list_burning_episodes',cover)
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(pluginhandle)
    
def list_burning_episodes():
    id = args['url'][0]
    myanime = args['name'][0]
    episodes = burning.get_episodes(id)
    for episode in episodes:
        epi = episode['epi']
        titlede = episode['german']
        titleen = episode['english']
        if titlede:
            name = myanime + 'E0' + epi + '. ' + titlede
        elif titleen:
            name = myanime + 'E0' + epi + '. ' + titleen
        else:
            name = myanime + 'E0' + epi
        name = name.encode('UTF-8')
        new_id = '%s%s/' % (id, str(epi))
        addEpisode('burning',name,new_id,'play_burning','','')
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(pluginhandle)

def get_mirrors():
    site = args['site'][0]
    anime = args['anime'][0]
    episode = args['episode'][0]
    if site == 'genx':
        aid = args['url'][0]
        hoster_list = genx.get_final_hoster_list(aid, episode)
    else:
        hoster_list = args['url']
    for mirror_site in mirror_sites:
        if not site in str(mirror_site):
            mirror = mirror_site.get_mirror(anime, episode)
            if mirror: hoster_list.append(mirror)
    play(hoster_list)
    
def play_burning():
    id = args['url'][0]
    hoster_list = burning.get_final_hoster_list(id)
    play(hoster_list)

def play(hoster_list):
    from resources.lib import resolver
    hoster_list = sort_hoster_list(hoster_list)
    print 'Hoster Liste: '+str(hoster_list)
    file = resolver.get_file(hoster_list)
    if file:
        listitem = xbmcgui.ListItem(path=file)
        if 'crunchyroll' in file:
            try:
                subtitle = common.get_subtitle()
                listitem.setSubtitles([subtitle])
            except:
                xbmc.executebuiltin('Notification(Kodi Required For Subtitles,)')
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
    else:
        xbmc.executebuiltin('Notification(No Stream Available,)')
        
def play_amv():
    name = args['name'][0]
    if name == 'AMV TV':
        playlist = amvnews.amv_tv()
        xbmc.Player().play(playlist)
    else:
        amv = amvnews.get_amv(name)
        if amv:
            file = amv['url']
            name = amv['name']
            li = xbmcgui.ListItem(name)
            xbmc.Player().play(file, listitem=li)
        else:
            xbmc.executebuiltin('Notification(No AMV Available,)')
            
def play_trailer():
    name = args['name'][0]
    trailer = anisearch.get_trailer(name)
    if trailer:
        from resources.lib import resolver
        file = resolver.get_file([[trailer]])
        li = xbmcgui.ListItem(name)
        xbmc.Player().play(file, listitem=li)
    else:
        xbmc.executebuiltin('Notification(No Trailer Available,)')

def sort_hoster_list(links):
    ehost1 = [i for i in links if addon.getSetting('ehost1') in i]
    ehost2 = [i for i in links if addon.getSetting('ehost2') in i]
    ehost3 = [i for i in links if addon.getSetting('ehost3') in i]
    ehost4 = [i for i in links if addon.getSetting('ehost4') in i]
    ehost5 = [i for i in links if addon.getSetting('ehost5') in i]
    ehost6 = [i for i in links if addon.getSetting('ehost6') in i]
    ehost7 = [i for i in links if addon.getSetting('ehost7') in i]
    ihost1 = [i for i in links if addon.getSetting('ihost1') in i]
    ihost2 = [i for i in links if addon.getSetting('ihost2') in i]
    ihost3 = [i for i in links if addon.getSetting('ihost3') in i]
    ihost6 = [i for i in links if addon.getSetting('ihost6') in i]
    ihost7 = [i for i in links if addon.getSetting('ihost7') in i]
    ihost8 = [i for i in links if addon.getSetting('ihost8') in i]
    ihost9 = [i for i in links if addon.getSetting('ihost9') in i]
    ihost10 = [i for i in links if addon.getSetting('ihost10') in i]
    if prefer_ihosts: return [ihost1,ihost2,ihost3,ihost6,ihost7,ihost8,ihost9,ihost10,ehost1,ehost2,ehost3,ehost4,ehost5,ehost6,ehost7]
    else: return [ehost1,ehost2,ehost3,ehost4,ehost5,ehost6,ehost7,ihost1,ihost2,ihost3,ihost6,ihost7,ihost8,ihost9,ihost10]
    
def clear_cache():
    try:
        common.clear_cache()
        addon.setSetting(id='clear_cache', value='false')
        xbmc.executebuiltin('Notification(Cache Deleted,)')
    except:
        xbmc.executebuiltin('Notification(Error While Deleting Cache,)')
    
def build_url(query):
	return sys.argv[0] + '?' + urllib.urlencode(query)

def addEpisode(site,name,url,mode,anime,episode):
    u = build_url({'site': site, 'mode': mode, 'name': name, 'url': url, 'anime': anime, 'episode': episode})
    item=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage='')
    item.setInfo( type="Video", infoLabels={ "Title": name } )
    item.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item)

def addAnime(site,name,url,mode,iconimage,plot,genre,year,episodes,episodes_aired,cm):
    if not iconimage: iconimage = image
    u = build_url({'site': site, 'mode': mode, 'name': name, 'url': url, 'iconimage': iconimage})
    item=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    item.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Genre": genre, "Year": year, "Episode": episodes, "Studio": site } )
    amv_uri=build_url({'mode': 'play_amv', 'name': name})
    cm.append( ('Play AMV', "XBMC.RunPlugin(%s)" % amv_uri) )
    trailer_uri=build_url({'mode': 'play_trailer', 'name': name})
    cm.append( ('Play Trailer', "XBMC.RunPlugin(%s)" % trailer_uri) )
    similar_uri=build_url({'mode': 'show_similar', 'name': name})
    cm.append( ('Show Similar', "Container.Update(%s)" % similar_uri) )
    item.addContextMenuItems( cm )
    xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item,isFolder=True)

def addDir(name,url,mode,iconimage):
    if not iconimage: iconimage = image
    u = build_url({'mode': mode, 'name': name, 'url': url, 'iconimage': iconimage})
    item=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item,isFolder=True)

args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)
print 'Arguments: '+str(args)

if mode==None:
    root()
else:
    exec '%s()' % mode[0]


