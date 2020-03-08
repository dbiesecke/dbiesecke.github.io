# -*- coding: utf-8 -*-

import xbmc,os,re,time
import json
from resources.lib import simple_requests as requests
from resources.lib import json_handle
from resources.lib import common
from random import randint

base_url = 'http://amvnews.ru'
abc_url = base_url+'/index.php?go=Anime&letter=%s&lang=en'
amv_tv_url = base_url+'/index.php?go=Files&in=newfiles&per=4&lang=en'
amv_quality = common.get_amv_quality()
timeout = common.get_timeout()

def amv_tv():
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    try:
        content = get_content(amv_tv_url)
        last = re.findall('<a class=newstitle href=.+?id=(.*?)>', content)
        a = 1
        while a < 101:
            a += 1
            r = randint(1,int(last[0]))
            amv = base_url+'/index.php?go=Files&file=down&id=%s' % str(r)
            if amv_quality == 'Low': amv = amv+'&alt=4'
            playlist.add(amv)
    except:
        pass
    return playlist

def get_amv(name):
    amv = ''
    try:
        abc = name[0]
        if not abc.isalpha(): abc = '0..9'
        else: abc.upper()
        anime_list = get_abc_series(abc)
        match = common.find_anime(name, anime_list, clean_burning=True)
        id = match[0]['id']
        content = get_content(base_url+id)
        amvs = re.findall('<tbody>(.*?)</tbody>', content, re.DOTALL)[0]
        amv = re.findall('<tr class="ratesrow.*?<a href="(.*?)"><span>(.*?)</span>', amvs)
        r = randint(0,len(amv))-1
        name = amv[r][1]
        amv = amv[r][0].replace("in=view","file=down")
        if amv_quality == 'Low': amv = amv+'&alt=4'
        amv = {'name': name, 'url': base_url+amv}
    except:
        pass
    return amv

def get_abc_series(abc):
    url = abc_url % abc
    anime_list = get_anime_list(url)
    return anime_list
    
def get_anime_list(url):
    anime_list = []
    content = get_content(url)
    anime_table = re.findall('<table class="anime_table"(.*?)</table>', content, re.DOTALL)[0]
    items = re.findall('<tr class="anime_tablerow(.*?)</tr>', anime_table, re.DOTALL)
    for item in items:
        name = re.findall('<a href=".*?">(.+?)</a>', item)[0]
        #name = name.encode('utf-8')
        url = re.findall('<a href="(.*?)">', item)[0]
        anime = ({'original': name, 'id': url})
        anime_list.append(anime)
    return anime_list
    
def get_content(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:27.0) Gecko/20100101 Firefox/27.0'}
	content = requests.get(url, headers=headers, timeout=timeout).text
	content = content.decode('windows-1251').encode('utf-8', 'ignore')
	content = content.replace("\n","").replace("\t","").replace("&amp;","&").replace("&ndash;","-").replace("<BR>","").replace("</B>","</b>").replace(' title="Socks5 proxy 50"','')
	return content