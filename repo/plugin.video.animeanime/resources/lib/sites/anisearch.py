# -*- coding: utf-8 -*-

import xbmc,os,re,time
import json
from resources.lib import simple_requests as requests
from resources.lib import json_handle
from resources.lib import common

site = 'anisearch'
base_url = 'http://de.anisearch.com/'
anime_url = base_url+'anime/%s'
streams_url = base_url+'anime/streams?sort=title'
search_url = base_url+'ajax/search/anime'
timeout = common.get_timeout()

def get_mirror(anime,episode):
    mirror = []
    try:
        anime_list = get_anime_list()
        match = common.find_anime(anime, anime_list)[0]
        id = match['id']
        episodes = get_episodes(id)
        for epi in episodes:
            if epi['episode'] == episode:
                mirror = epi['url']
    except:
        pass
    return mirror

def get_anime_list():
    cache_url = common.cleanfilename(streams_url)
    anime_list = json_handle.load_json(site, cache_url, cache_time=7)
    if anime_list:
        return anime_list
    else:
        anime_list = []
        try:
            content = requests.get(streams_url).text
            re_pages = re.findall('<span class="pagenav-pages">Seite 1 von (\d+)</span>', content, re.DOTALL)[0]
            for i in range(1, int(re_pages)+1):
                url = streams_url+'&page='+str(i)
                content = requests.get(url, timeout=timeout).text
                index = re.findall('<table class="index-gallery">(.*?)</table>', content, re.DOTALL)[0]
                items = re.findall('<td><a(.*?)</td>', index, re.DOTALL)
                for item in items:
                    #if 'TV,' in item:
                        url = re.findall('href="(.*?)"', item, re.DOTALL)[0]
                        cover = re.findall('<img src="(.*?)"', item, re.DOTALL)[0]
                        cover = cover.replace('thumb','full')
                        name = re.findall('alt="(.+?)"', item, re.DOTALL)[0]
                        try: year = re.findall('advinfo mtA.*?([0-9]{4})', item, re.DOTALL)[0]
                        except: year = ''
                        try: genre = re.findall('advinfoB.*?gt;(.*?)&lt', item, re.DOTALL)[0]
                        except: genre = ''
                        anime_list.append({'site': site, 'original': name, 'id': url, 'cover': cover, 'year': year, 'genre': genre})
            if anime_list: json_handle.save_json(site, cache_url, anime_list)
        except:
            pass
        return anime_list
        
def get_anime_info(id):
    return []

def get_abc_series(abc):
    abc_list = []
    if abc == 'num': abc = ('.','0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    elif abc == 'all': abc = ''
    else: abc = abc.lower()
    anime_list = get_anime_list()
    if abc:
        for anime in anime_list:
            if anime['original'].lower().startswith(abc):
                abc_list.append(anime)
    else:
        abc_list = anime_list
    return abc_list
        
def get_new_series():
    return []
        
def get_episodes(id):
    cache_url = common.cleanfilename(id)
    episodes = json_handle.load_json(site, cache_url+'episodes', cache_time=1)
    if episodes:
        return episodes
    else:
        episodes = []
        try:
            content = requests.get(base_url+id, timeout=timeout).text
            url = re.findall('<ul class="streams"><li><a href="(.*?)"', content, re.DOTALL)[0]
            url = url.replace('amp;','')
            content = requests.get(base_url+url, timeout=timeout).text
            streamlist = re.findall('<div class="title"><h2>Streams(.*?)</ul>', content, re.DOTALL)[0]
            items = re.findall('<stro(.*?)</li>', streamlist, re.DOTALL)
            for item in items:
                url = re.findall('href="(.*?)"', item)[0]
                title = re.findall('ng>(.*?)</strong>', item)[0]
                try:
                    episode = re.findall(r'\d+', title)[0]
                    while episode.startswith('0'):
                        episode = episode[1:]
                except:
                    episode = 0
                episodes.append({'name': title, 'url': url, 'episode': episode})
            if episodes: json_handle.save_json(site, cache_url+'episodes', episodes)
        except:
            pass
        return episodes

def get_trailer(name):
    aid = search(name)
    try:
        content = requests.get(anime_url % str(aid), timeout=timeout).text
        match = re.findall('<a itemprop="trailer" href="(.*?)"', content, re.DOTALL)
        for trailer in match:
            if 'youtube' in trailer:
                return trailer
    except:
        pass
        
def get_similar(name):
    anime_list = []
    aid = search(name)
    try:
        content = requests.get(anime_url % str(aid)+'/relations#similar', timeout=timeout).text
        similar = re.findall('<a id="recommendations">(.*?)</main>', content, re.DOTALL)[0]
        items = re.findall('<img src="(.*?)" alt="(.*?)"', similar, re.DOTALL)
        for cover, name in items:
            anime_list.append({'original': name.decode('utf-8'), 'cover': cover})
        return anime_list
    except:
        pass
        
def search(name):
    try:
        aid = None
        data = {"t": name.decode('utf-8'), "p": 0}
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        json_result = requests.post(search_url, headers=headers, data=data, timeout=timeout).json()
        result = json_result['r']
        for anime in result:
            if name == anime['t']:
                aid = anime['i']
        if not aid:        
            aid = json_result['r'][0]['i']
        return aid
    except:
        pass