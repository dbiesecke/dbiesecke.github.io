# -*- coding: utf-8 -*-

import os,re,xbmc,xbmcaddon,shutil,json

addon = xbmcaddon.Addon(id='plugin.video.animeanime')
datapath = xbmc.translatePath('special://profile/addon_data/plugin.video.animeanime')
if not os.path.isdir(datapath):
  os.mkdir(datapath)

def get_addon():
    return addon
    
def clear_cache():
    folders = [ name for name in os.listdir(datapath) if os.path.isdir(os.path.join(datapath, name)) ]
    for folder in folders:
        shutil.rmtree(os.path.join(datapath, folder))

def get_image():
    home = addon.getAddonInfo('path').decode('utf-8')
    image = xbmc.translatePath(os.path.join(home, 'icon.png'))
    return image
    
def get_subtitle():
    subtitle = os.path.join(datapath,'subtitle.ass')
    return subtitle
    
def get_timeout():
    timeout = addon.getSetting('timeout')
    return int(timeout)
    
def get_amv_quality():
    amv_quality = addon.getSetting('amv_quality')
    return amv_quality

def find_anime(name, anime_list, clean_burning=False):
    anime = []
    try: anime = [i for i in anime_list if name == i['original'].encode('utf-8')]
    except: anime = [i for i in anime_list if name == i['original']]
    if not anime and len(name) > 5:
        name = cleantitle(name, clean_burning)
        anime = [i for i in anime_list if name == cleantitle(i['original'], clean_burning)]
        if not anime: anime = [i for i in anime_list if name in cleantitle(i['original'], clean_burning)]
        if not anime and clean_burning: anime = [i for i in anime_list if cleantitle(i['original'], clean_burning) in name]
    return anime

def remove_duplicates(list):
    all_ids = [ cleantitle(each['original'], clean_burning=False) for each in list ]
    anime_list = [ list[ all_ids.index(id) ] for id in set(all_ids) ]
    return anime_list
    
def cleantitle(title, clean_burning):
    try: title = title.encode('utf-8')
    except: pass
    if clean_burning:
        new_title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\!|\?|\=|\&|/)|\s|(\d{4})|(\d{1})|([(])|([)])', '', title).lower() 
    else:
        new_title = re.sub('\n|([[].+?[]])|\s(vs|v[.])\s|(:|;|-|"|,|\.|\!|\?|\=|\&|/)|\s|([(])|([)])', '', title).lower()
    new_title = re.sub("\’", "'", new_title)
    if len(title) > 4: return new_title
    else: return title
    
def cleanfilename(title):
    title = re.sub('(:|;|-|"|,|\'|\.|\?|\=|\&|/)', '', title).lower()
    return title