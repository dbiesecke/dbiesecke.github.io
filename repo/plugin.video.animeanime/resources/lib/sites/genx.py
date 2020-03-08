# -*- coding: utf-8 -*-

import xbmc,os,re,time
import json
from resources.lib import simple_requests as requests
from resources.lib import json_handle
from resources.lib import common

site = 'genx'
base_url = 'http://www.genx-anime.org/'
search_url = base_url+'index.php?do=display&q='
ajax_url = base_url+'ajax/'
details_url = ajax_url+'calendar_details.inc.php'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:27.0) Gecko/20100101 Firefox/27.0', 'Host':'www.genx-anime.org'}
timeout = common.get_timeout()

def get_airing_anime_aids(url):
    aids = json_handle.load_json(site, 'airing', cache_time=7)
    if aids:
        return aids
    else:
        aids = []
        data = {'offset': '0', 'limit': '100', 'status': '0'}
        url = ajax_url+url
        try:
            content = requests.post(url, headers=headers, data=data, timeout=timeout).text
            re_aid = re.findall('data-aid="(.*?)"', content)
            for aid in re_aid:
                if not aid == '0':
                    aids.append({ 'aid': aid })
            json_handle.save_json(site, 'airing', aids)
        except:
            pass
        return aids
        
def get_search_aids(search_entered=False):
    if not search_entered:
        kb = xbmc.Keyboard('', 'Suche', False)
        kb.doModal()
        search_entered = kb.getText().replace(' ','+')
    final_url = search_url+search_entered
    aids = []
    try:
        content = requests.get(final_url, headers=headers, timeout=timeout).text
        re_aid = re.findall('upload/cover/.*?/(\d+).png', content)
        for aid in re_aid:
            if not aid == '0':
                aids.append({ 'aid': aid })
            if len(aids) > 19:
                break
    except:
        pass
    return aids

def get_genres():
    genres = ['Abenteuer', 'Action', 'Actiondrama', 'Actionkom\xc3\xb6die', 'Alltagsdrama', 'Drama',
                'Fighting-Shounen', 'Ganbatte', 'Geistergeschichten', 'Genre-Mix', 'Hentai', 'Horror', 
                'Kom\xc3\xb6die', 'Krimi', 'Liebesdrama', 'Nonsense-Kom\xc3\xb6die',
                'Romantische Kom\xc3\xb6die', 'Romanze', 'Sentimentales Drama', 'Thriller']
    return genres

def get_alphabet():
    alphabet = ['num', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    return alphabet
    
def get_anime_list_html(url, cache_time=False):
    cache_url = common.cleanfilename(url)
    anime_list = json_handle.load_json(site, cache_url, cache_time=1)
    if anime_list:
        return anime_list
    else:
        anime_list = []
        try:
            content = requests.get(base_url+url, headers=headers, timeout=timeout).text
            re_pages = re.findall('<dt style=.*?</dt>', content, re.DOTALL)[0]
            re_pages = re.findall('href="(.*?)"', re_pages)
        except:
            re_pages = [url]
        try:
            for url in re_pages:
                content = requests.get(base_url+url, headers=headers, timeout=timeout).text
                items = re.findall('<li class="item">.*?</li>', content, re.DOTALL)
                for item in items:
                    url = re.findall('href="(.+?)"', item)[0]
                    id = url.split('id=')[-1]
                    id = id.split()[0]
                    name = re.findall('</span>">(.+?)</span>', item)[0]
                    try:
                        genres = re.findall('Genre</strong>: (.*?)<br/>', item)[0]
                        try: genre = genres.split(',')
                        except: genre = [genres]
                    except: genre = []
                    try: setting = re.findall('Setting</strong>: (.*?)<br/>', item)[0]
                    except: setting = ''
                    plot = re.findall('<br/><br/>(.*?)</span>', item, re.DOTALL)[0]
                    plot = plot.replace("&quot;","'")
                    year = re.findall('<dt class="ayear">.*?([0-9]{4}).*?</dt>', item, re.DOTALL)[0]
                    episodes = re.findall('<dt class="aepisode">.*?\/.*?(\d+).*?</dt>', item, re.DOTALL)[0]
                    episodes_aired = re.findall('<dt class="aepisode">.*?(\d+).*?\/', item, re.DOTALL)[0]
                    languages = re.findall('<img title="(.*?)"', item)
                    languages = ', '.join(languages).replace('Enth\xc3\xa4lt ','')
                    anime_list.append({ 'id': id, 'beschreibung': plot, 'folgenzahl': episodes,
                                        'genre': genre, 'length': episodes_aired, 'original': name,
                                        'setting': setting, 'languages': languages, 'year': year })
            json_handle.save_json(site, cache_url, anime_list)
        except:
            pass
        return anime_list
    
def get_anime_list(aids):
    if 'index.php' in aids:
        anime_list = get_anime_list_html(aids)
    else:
        anime_list = []
        for aid in aids:
            json_data = get_anime_info(aid)
            anime_list.append(json_data)
    return anime_list

def get_episodes(aid):
    json_data = get_anime_info(aid, cache_time=1)
    try: episodes = json_data['folgen']
    except: episodes = ''
    return episodes

def get_final_hoster_list(aid, episode):
    hoster_list = get_hoster_list(aid, episode)
    links = []
    for hoster in hoster_list:
        link = hoster['link']
        links.append(link)
    return links

def get_hoster_list(aid, episode):
    episodes = get_episodes(aid)
    try: hoster_list = episodes[episode]['Stream']
    except: hoster_list = ''
    return hoster_list

def get_anime_info(aid, cache_time=False):
    try: aid = aid['aid']
    except: pass
    data = {'aid': str(aid)}
    json_data = ''
    json_data = json_handle.load_json(site, aid, cache_time)
    if json_data:
        return json_data
    else:
        try: 
            json_data = requests.post(details_url, headers=headers, data=data, timeout=timeout).json()
            json_handle.save_json(site, aid, json_data)
        except:
            pass
        return json_data