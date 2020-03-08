# -*- coding: utf-8 -*-

import xbmc,os
import json,time
import shutil

def get_datapath(site):
    datapath = xbmc.translatePath('special://profile/addon_data/plugin.video.animeanime/%s/' % site)
    if not os.path.isdir(datapath):
        os.mkdir(datapath)
    return datapath

def load_json(site, id, cache_time=False):
    if not cache_time: cache_time = 7
    try:
        datapath = get_datapath(site)
        json_file = os.path.join(datapath,'%s.json' % id)
        if os.path.exists(json_file):
            modified_time = round(os.stat(json_file).st_mtime)
            current_time = round(time.time())
            t = current_time - modified_time
            if (t / 3600) > 24*cache_time: return
            with open(json_file) as f:
                json_data = json.load(f)
            return json_data
        else:
            return
    except:
        pass

def save_json(site, id, json_data):
    try:
        datapath = get_datapath(site)
        json_files = [f for f in os.listdir(datapath) if f.endswith('.json')]
        if len(json_files) > 150:
            shutil.rmtree(datapath)
        json_file = os.path.join(datapath,'%s.json' % id)
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
    except:
        pass