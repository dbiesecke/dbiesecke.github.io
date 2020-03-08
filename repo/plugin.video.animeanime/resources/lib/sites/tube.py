# -*- coding: utf-8 -*-

import xbmc,os,re,time
import json
from resources.lib import simple_requests as requests
from resources.lib import json_handle
from resources.lib import common

site = 'tube'
base_url = 'http://www.anime-tube.tv'
series_url = base_url+'/animeliste-1'
movies_url = base_url+'/animeliste-2'
ovas_url = base_url+'animeliste-3'
specials_url = base_url+'/animeliste-4'
timeout = common.get_timeout()

def get_mirror(anime,episode):
    mirror = []
    try:
        abc = anime[0]
        if not abc.isalpha():
            abc = 'num'
        anime_list = get_abc_series(abc)
        match = common.find_anime(anime, anime_list)
        if 'One Piece' in anime and episode > 401: match = match[1]
        else: match = match[0]
        id = match['id']
        episodes = get_episodes(id)
        for epi in episodes:
            if epi['episode'] == episode:
                mirror = epi['url']
    except:
        pass
    return mirror

def get_anime_list(url):
    cache_url = common.cleanfilename(url)
    anime_list = json_handle.load_json(site, cache_url, cache_time=1)
    if anime_list:
        return anime_list
    else:
        anime_list = []
        abc_url = url
        try:
            content = requests.get(url, timeout=timeout).text
            re_pages = re.findall('/><div><center>.*?</center></div><br></div></div>', content)[0]
            re_pages = re.findall('<a href=".*?">(.*?)</a>', re_pages)[-1]
        except:
            re_pages = 1
        try:
            for i in range(0, int(re_pages)):
                url = abc_url.replace('.html','-'+str(i+1)+'.html')
                content = requests.get(url, timeout=timeout).text
                items = re.findall('<div class="group">(.*?<div class="title">.*?<div class="meta_r".*?</div>)', content, re.DOTALL)
                for item in items:
                    url = re.findall('<a href=".(/anime.*?html)"', item)[0]
                    name = re.findall('title="(.+?)"', item)[0]
                    cover = re.findall('src="(.*?)"', item)[0]
                    try: cover = cover.replace(' ','%20')
                    except: pass
                    try:
                        plot = re.findall('<div class="meta_r".*?>(.+)</div>', item, re.DOTALL)[0]
                        plot = plot.decode('utf-8')
                        plot = plot.replace('&hellip;', '...')
                    except:
                        plot = ''
                    try: year = re.findall('Jahr</b>: ([0-9]{4})', item)[0]
                    except: year = ''
                    anime_list.append({'site': site, 'original': name, 'id': url, 'cover': cover, 'year': year, 'beschreibung': plot})
            if anime_list: json_handle.save_json(site, cache_url, anime_list)
        except:
            pass
        return anime_list
    
def get_abc_series(abc):
    abc_list = []
    if abc == 'num': abc = '1'
    elif abc == 'all': pass
    else: abc = abc.upper()
    url = series_url+'-'+abc+'.html'
    anime_list = get_anime_list(url)
    return anime_list
    
def get_new_series():
    new_list = []
    try:
        content = requests.get(base_url, timeout=timeout).text
        new = re.findall('Die letzten Anime Uploads(.*?)</ul>', content, re.DOTALL)[0]
        items = re.findall('<li style(.*?)</li>', new, re.DOTALL)
        for item in items:
            cover = re.findall('<div style="background-image: url\(.(.+?)\)', item, re.DOTALL)[0]
            id = cover.split('=')[-1]
            url = '/anime-%s.html' % id
            name = re.findall('<div style="text-decoration.*?>(.+?)<', item, re.DOTALL)[0]
            new_list.insert(0, {'site': site, 'original': name, 'id': url, 'cover': base_url+cover})
    except:
        pass
    return new_list

def get_anime_info(id):
    cache_url = common.cleanfilename(id)
    anime = json_handle.load_json(site, cache_url, cache_time=7)
    if anime:
        return anime
    else:
        anime = []
        try:
            content = requests.get(base_url+id, timeout=timeout).text
            name = re.findall('<li><b>Titel</b>: (.+?)</li>', content)[0]
            plot = re.findall('<li><b>Beschreibung</b>: (.*?)</li>', content, re.DOTALL)[0]
            genres = re.findall('<li><b>Genre</b>: (.*?)</li>', content)[0]
            try: genre = genres.split(',')
            except: genre = [genres]
            year = re.findall('<li><b>Jahr</b>: (.*?)</li>', content)[0]
            cover = re.findall('<div class="thumbnail".*?<img src="(.*?)"', content, re.DOTALL)[0]
            anime = ({'site': site, 'original': name, 'id': id, 'cover': cover, 'beschreibung': plot, 'genre': genre, 'year': year})
            json_handle.save_json(site, cache_url, anime)
        except:
            pass
        return anime

def get_episodes(id):
    cache_url = common.cleanfilename(id)
    episodes = json_handle.load_json(site, cache_url+'episodes', cache_time=1)
    if episodes:
        return episodes
    else:
        episodes = []
        try:
            content = requests.get(base_url+id, timeout=timeout).text
            re_pages = re.findall("(/anime-.*?-.*?.html)'>", content)
            for page in re_pages:
                url = base_url+page
                content = requests.get(url, timeout=timeout).text
                items = re.findall('<div class="element">(.*?)<div class="meta_r">', content, re.DOTALL)
                for item in items:
                    url = re.findall('href=".(.*?)"', item)[0]
                    title = re.findall('title="(.*?)"', item)[0]
                    episode = re.findall(r'\d+', title)[0]
                    episodes.append({'name': title, 'url': base_url+url, 'episode': episode})
            if episodes: json_handle.save_json(site, cache_url+'episodes', episodes)
        except:
            pass
        return episodes