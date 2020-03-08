# -*- coding: utf-8 -*-

import xbmc,os,re,time
import json
from resources.lib import simple_requests as requests
from resources.lib import json_handle
from resources.lib import common

site = 'tavernakoma'
base_url = 'http://www.tavernakoma.net'
video_url = 'http://tavernakoma.net/video.php'
list_url = base_url+'/list.php'
timeout = common.get_timeout()

def get_mirror(anime,episode):
    mirror = []
    try:
        anime_list = get_complete_anime_list()
        match = common.find_anime(anime, anime_list)[0]
        id = match['id']
        episodes = get_episodes(id)
        for epi in episodes:
            if epi['episode'] == episode:
                mirror = epi['url']
    except:
        pass
    return mirror

def get_complete_anime_list():
    cache_url = common.cleanfilename(list_url)
    anime_list = json_handle.load_json(site, cache_url, cache_time=1)
    if anime_list:
        return anime_list
    else:
        anime_list = []
        try:
            content = requests.get(list_url, timeout=timeout).text
            animetable = re.findall('<ul id="animetable">(.*?)</table>', content, re.DOTALL)[0]
            liste = re.findall('<a href="(.*?)"><li>(.+?)</li></a>', animetable, re.DOTALL)
            for url, name in liste:
                c = url.split('page=')[-1]
                cover = 'http://tavernakoma.net/images/player/%s.jpg' % c
                anime_list.append({'site': site, 'original': name, 'id': url, 'cover': cover, 'beschreibung': ''})
            json_handle.save_json(site, cache_url, anime_list)
        except:
            pass
        return anime_list
    
def get_anime_list(ids):
    anime_list = []
    for id in ids:
        anime = get_anime_info(id)
        anime_list.append(anime)
    return anime_list

def get_abc_series(abc):
    abc_list = []
    if abc == 'num': abc = ('.','0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    elif abc == 'all': abc = ''
    else: abc = abc.lower()
    anime_list = get_complete_anime_list()
    if abc:
        for anime in anime_list:
            if anime['original'].lower().startswith(abc):
                abc_list.append(anime)
    else:
        abc_list = anime_list
    return abc_list

def get_new_series():
    return []

def get_anime_info(id):
    cache_url = common.cleanfilename(id)
    anime = json_handle.load_json(site, cache_url, cache_time=7)
    if anime:
        return anime
    else:
        anime = []
        try:
            content = requests.get(base_url+id, timeout=timeout).text
            c = id.split('page=')[-1]
            name = re.findall('<article><h4>(.+?)</h4></article>', content, re.DOTALL)[0]
            cover = 'http://tavernakoma.net/images/player/%s.jpg' % c
            try: beschreibung = re.findall('<div class="anime-description">(.*?)</div>', content, re.DOTALL)[0]
            except: beschreibung = ''
            try:
                genres = []
                genrelist = re.findall('<ul id="genrelist">(.*?)</ul>', content, re.DOTALL)[0]
                match = re.findall('<li>(.*?)</li>', genrelist, re.DOTALL)
                for genre in match:
                    genres.append(genre)
            except: genres = []
            anime = ({'site': site, 'original': name, 'id': id, 'cover': cover, 'beschreibung': beschreibung, 'genre': genres})
            if anime: json_handle.save_json(site, cache_url, anime)
        except:
            pass
        return anime

def get_episodes(id):
    episodes = []
    try:
        active = id.split('page=')[-1]
        headers = {'Cookie': 'active='+active}
        content = requests.get(video_url, headers=headers, timeout=timeout).text
        items = re.findall('<item>(.*?)</item>', content, re.DOTALL)
        for item in items:
            title = re.findall('<title>(.*?)</title>', item)[0]
            episode = re.findall(r'\d+', title)[0]
            while episode.startswith('0'):
                episode = episode[1:]
            link = re.findall('file="(.*?)"', item)[0]
            episodes.append({'name': title, 'url': link, 'episode': str(episode)})
    except:
        pass
    return episodes