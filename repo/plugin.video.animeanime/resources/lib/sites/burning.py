
# -*- coding: utf-8 -*-

import xbmc,os,re,time
import json
from resources.lib import simple_requests as requests
from resources.lib import json_handle
from resources.lib import common

site = 'burning'
api_url = 'https://www.burning-seri.es/api/'
genre_url = api_url+'series:genre/'
series_url = api_url+'series/'
cover_url = 'https://s.burning-seri.es/img/cover/%s.jpg'
timeout = common.get_timeout()

def get_burning_seasons(name):
    burning_seasons = []
    anime_list = get_complete_anime_list()
    animename = name
    match = common.find_anime(name, anime_list, clean_burning=True)
    for series in match:
        b_id = series['id']
        b_name = series['original']
        cover = 'https://s.burning-seri.es/img/cover/%s.jpg' % b_id
        seasons = get_seasons(b_id)
        for i in range(int(seasons)):
            name = animename+'.S0%s' % str(i+1)
            id = '%s/%s/' % (str(b_id), str(i+1))
            burning_seasons.append({'name': name, 'id':id, 'cover': cover})
    return burning_seasons
    
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
    anime = []
    try:
        json_data = get_anime_json(id)
        name = json_data['series']['series'].encode('UTF-8')
        id = json_data['series']['id']
        cover = 'https://s.burning-seri.es/img/cover/%s.jpg' % id
        try: beschreibung = json_data['series']['description']
        except: beschreibung = ''
        try: year = json_data['series']['start']
        except: year = ''
        try: genres = json_data['series']['data']['genre']
        except: genres = []
        anime = ({'site': site, 'original': name, 'id': id, 'cover': cover, 'beschreibung': beschreibung, 'year': year, 'genre': genres})
    except:
        pass
    return anime
    
def get_complete_anime_list():
    cache_url = common.cleanfilename(genre_url)
    anime_list = json_handle.load_json(site, cache_url, cache_time=1)
    if anime_list:
        return anime_list
    else:
        anime_list = []
        genre = 'Anime'
        try:
            json_data = requests.get(genre_url, timeout=timeout).json()
            series = json_data[genre]['series']
            for serie in series:
                name = serie['name'].encode('UTF-8')
                id = serie['id']
                cover = 'https://s.burning-seri.es/img/cover/%s.jpg' % id
                anime_list.append({'site': site, 'original': name, 'id': id, 'cover': cover, 'beschreibung': '', 'year': '', 'genre': ''})
            json_handle.save_json(site, cache_url, anime_list)
        except:
            pass
        return anime_list

def get_anime_list(bids):
    anime_list = []
    for id in bids:
        anime = get_anime_info(id)
        anime_list.append(anime)
    return anime_list
    
def get_anime_json(id):
    json_data = ''
    site = 'burning'
    json_data = json_handle.load_json(site, id)
    if json_data:
        return json_data
    else:
        try:
            url = series_url+str(id)+'/1/'
            json_data = requests.get(url, timeout=timeout).json()
            json_handle.save_json(site, id, json_data)
        except:
            pass
        return json_data
    
def get_seasons(id):
    seasons = []
    try:
        json_data = get_anime_json(id)
        seasons = json_data['series']['seasons']
    except:
        pass
    return seasons

def get_episodes(id):
    episodes = []
    try:
        url = series_url+id
        json_data = requests.get(url, timeout=timeout).json()
        episodes = json_data['epi']
    except:
        pass
    return episodes
    
def get_final_hoster_list(id):
    links = []
    hoster_list = get_hoster(id)
    for hoster in hoster_list:
        id = hoster['id']
        link = get_stream_link(id)
        links.append(link)
    return links

def get_hoster(id):
    hoster = []
    try:
        url = series_url+id
        json_data = requests.get(url, timeout=timeout).json()
        hoster = json_data['links']
    except:
        pass
    return hoster
    
def get_stream_link(id):
    link = []
    try:
        watch_url = api_url+'watch/%s' % id
        json_data = requests.get(watch_url).json()
        link = json_data['fullurl']
    except:
        pass
    return link
