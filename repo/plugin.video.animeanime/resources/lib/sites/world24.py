# -*- coding: utf-8 -*-

import xbmc,os,re,time
import json
from resources.lib import simple_requests as requests
from resources.lib import json_handle
from resources.lib import common

site = 'world24'
base_url = 'http://anime-world24.net/'
list_url = base_url+'animeliste'
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
            liste = re.findall('<tr id=(.*?)</tr>', content, re.DOTALL)
            for anime in liste:
                url = re.findall('href="(.*?)"', anime, re.DOTALL)[0]
                name = re.findall('class="cmc">(.+?)</a>', anime, re.DOTALL)[0]
                anime_list.append({'site': site, 'original': name, 'id': url, 'beschreibung': ''})
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
            match = re.findall('<li id="animedescriptionimg">.*?<img src="(.*?)" alt="(.+?)"', content, re.DOTALL)
            name = match[0][1]
            cover = match[0][0]
            try: plot = re.findall('Inhalt.*?<p>(.*?)</p>', content, re.DOTALL)[0]
            except: plot = ''
            try:
                genres = re.findall('Genre:.*?<p>(.*?)</p>', content, re.DOTALL)[0]
                try: genre = genres.split(',')
                except: genre = [genres]
            except : genre = []
            try: 
                year = re.findall('Release:.*?<p>(.*?)</p>', content, re.DOTALL)[0]
                year = year.split('.')[-1]
            except: year = ''
            anime = ({'site': site, 'original': name, 'id': id, 'cover': base_url+cover, 'beschreibung': plot, 'genre': genre, 'year': year})
            if anime: json_handle.save_json(site, cache_url, anime)
        except:
            pass
        return anime

def get_episodes(id):
    episodes = []
    try:
        content = requests.get(base_url+id, timeout=timeout).text
        folgen = re.findall('<h2>Folgen</h2>.*?href="(.*?)"', content, re.DOTALL)[0]
        content = requests.get(base_url+folgen, timeout=timeout).text
        item = re.findall('file: "(.+?)".*?title: "(.+?)".*?description: "(.+?)"', content, re.DOTALL)
        for file, title, description in item:
            name = title+' - '+description
            episode = re.findall(r'\d+', title)[0]
            while episode.startswith('0'):
                episode = episode[1:]
            episodes.append({'name': name, 'url': file, 'episode': episode})
    except:
        pass
    return episodes