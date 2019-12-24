import os
import re
import gzip
import shutil
import time
import json
import subprocess
import arrow

import xml.parsers.expat
from xml.sax.saxutils import escape
from urlparse import urlparse

import xbmc, xbmcaddon

from matthuisman import settings, userdata, database, gui
from matthuisman.constants import ADDON_ID, ADDON_DEV, ADDON_PROFILE
from matthuisman.log import log
from matthuisman.session import Session
from matthuisman.exceptions import Error
from matthuisman.util import remove_file

from .constants import FORCE_RUN_FLAG, PLAYLIST_FILE_NAME, EPG_FILE_NAME, METHOD_PLAYLIST, METHOD_EPG, MERGE_SETTING_FILE, IPTV_SIMPLE_ID, MERGE_START_WAIT, MERGE_TIMEOUT
from .models import Source, Channels, save_epg_channels
from .language import _

monitor  = xbmc.Monitor()

CHUNKSIZE = settings.getInt('chunksize', 4096)

def call(cmd):
    log.debug('Subprocess call: {}'.format(cmd))
    return subprocess.call(cmd)

def find_gz():
    log.debug('Searching for Gzip binary...')

    for gzbin in ['/bin/gzip', '/usr/bin/gzip', '/usr/local/bin/gzip', '/system/bin/gzip']:
        if os.path.exists(gzbin):
            log.debug('Gzip binary found: {}'.format(gzbin))
            return gzbin
    
    return None

def gzip_extract(in_path):
    log.debug('Gzip Extracting: {}'.format(in_path))

    out_path = in_path + '.extract'

    try:
        with open(out_path, 'wb') as f_out, gzip.open(in_path, 'rb') as f_in:
            shutil.copyfileobj(f_in, f_out, length=CHUNKSIZE)
    except IOError:
        log.debug('Failed to extract using python gzip (Known Kodi Android bug)')
        remove_file(out_path)
    else:
        shutil.move(out_path, in_path)
        return

    gzbin = find_gz()
    if not gzbin:
        remove_file(in_path)
        raise Error(_.NO_GZIP_BINARY)

    gz_path = in_path + '.gz'
    remove_file(gz_path)

    shutil.move(in_path, gz_path)
    call([gzbin, '-d', gz_path])
    
    if os.path.exists(gz_path):
        remove_file(gz_path)
        raise Error(_(_.GZIP_FAILED, path=gz_path))

def call_addon_method(plugin_url):
    xbmc.executebuiltin('Skin.SetString(merge,)')
    time.sleep(0.2)
    xbmc.executebuiltin('XBMC.RunPlugin({})'.format(plugin_url))

    value = ''
    for i in range(MERGE_START_WAIT):
        value = xbmc.getInfoLabel('Skin.String(merge)').lower()
        if value != '' or monitor.waitForAbort(1):
            break

    for i in range(MERGE_TIMEOUT):
        value = xbmc.getInfoLabel('Skin.String(merge)').lower()
        if value != 'started' or monitor.waitForAbort(1):
            break

    xbmc.executebuiltin('Skin.SetString(merge,)')

    if value != 'ok':
        if i == (MERGE_TIMEOUT-1):
            raise Error(_(_.ADDON_METHOD_TIMEOUT, url=plugin_url))
        else:
            raise Error(_(_.ADDON_METHOD_FAILED, url=plugin_url))

def process_file(item, method_name, file_path):
    if item.path_type == Source.TYPE_ADDON:
        addon      = xbmcaddon.Addon(item.path)
        addon_id   = addon.getAddonInfo('id')
        addon_path = xbmc.translatePath(addon.getAddonInfo('path')).decode("utf-8")
        merge_path = os.path.join(addon_path, MERGE_SETTING_FILE)

        with open(merge_path) as f:
            data = json.load(f)

        item.path = data[method_name].replace('$ID', addon_id).replace('$FILE', file_path)

        if item.path.lower().startswith('plugin'):
            call_addon_method(item.path)
            return

        if item.path.lower().startswith('http'):
            item.path_type = Source.TYPE_REMOTE
        else:
            item.path_type = Source.TYPE_LOCAL

        if item.path.lower().endswith('.gz'):
            item.file_type = Source.FILE_GZIP

    if item.path_type == Source.TYPE_REMOTE:
        log.debug('Downloading: {} > {}'.format(item.path, file_path))
        Session().chunked_dl(item.path, file_path)
        
    elif item.path_type == Source.TYPE_LOCAL:
        path = xbmc.translatePath(item.path)
        if not os.path.exists(path):
            raise Error(_(_.LOCAL_PATH_MISSING, path=path))
        
        log.debug('Copying local file: {} > {}'.format(path, file_path))
        shutil.copyfile(path, file_path)

    if item.file_type == Source.FILE_GZIP:
        gzip_extract(file_path)

def merge_playlists(playlists, output_dir):
    log.debug('Merging {} Playlists...'.format(len(playlists)))

    merged_path = os.path.join(output_dir, '.iptv_merge_playlist')

    channels    = []
    last_chn_no = 0

    for playlist in playlists:
        file_path = os.path.join(output_dir, '.iptv_merge_tmp')
        remove_file(file_path)
        process_file(playlist, METHOD_PLAYLIST, file_path)

        log.debug('Processing: {}'.format(playlist.path))
        with open(file_path, 'rb') as infile:
            found = None

            for line in infile:
                line = line.strip()

                if line.startswith('#EXTINF'):
                    found = line
                elif found and line and not line.startswith('#'):
                    data = {'_url': line, '_name': '', '_source': playlist.id}

                    parse = urlparse(data['_url'])
                    if not parse.scheme or not parse.netloc:
                        found = None
                        continue

                    colon = found.find(':', 0)
                    comma = found.rfind(',', 0)
                    
                    if colon >= 0 and comma >= 0 and comma > colon:
                        data['_name'] = found[comma+1:].strip()

                    for key, value in re.findall('([\w-]+)="([^"]*)"', found):
                        data[key] = value.strip()

                    channels.append(data)
                    found = None

        remove_file(file_path)

    Channels.set_channels(channels)

    with open(merged_path, 'wb') as outfile:
        outfile.write('#EXTM3U')

        for channel in Channels().playlist():
            id       = channel.pop('_id')
            hidden   = channel.pop('_hidden', settings.getBool('default_hidden', False))
            url      = channel.pop('_url', '')
            name     = channel.pop('_name', '')
            modified = channel.pop('_modified')
            source   = channel.pop('_source', None)
            added    = channel.pop('_added', None)

            if hidden:
                continue

            outfile.write('\n#EXTINF:-1')
            for key in channel:
                outfile.write(' {}="{}"'.format(key, unicode(channel[key]).encode('utf8')))

            outfile.write(',{}\n{}'.format(name.encode('utf8'), url))

    return merged_path

class Parser(object):
    def __init__(self, outfile):
        self._file = outfile

        self._skip_element = None
        self._current_channel = None
        self._last_data = None
        self._channels  = {}
        self._ignore_tags  = ['tv',]

    @property
    def channels(self):
        return self._channels

    def parse(self, file_path):
        parser = xml.parsers.expat.ParserCreate()
        parser.ordered_attributes = 1
        parser.StartElementHandler = self.start_element
        parser.EndElementHandler = self.end_element
        parser.CharacterDataHandler = self.char_data

        with open(file_path, 'rb') as infile:
            while True:
                chunk = infile.read(CHUNKSIZE)

                if len(chunk) < CHUNKSIZE:
                    parser.Parse(chunk, 1)
                    break

                parser.Parse(chunk)

    def char_data(self, data):
        if self._skip_element:
            return

        data = data.replace('&', '&amp;')
        data = data.replace('<', '&lt;')
        if data == '>':
            data = '&gt;'

        data = data.strip()

        self._last_data = data

        if data:
            self._file.write(data.encode('utf8'))

    def end_element(self, name):
        if name in self._ignore_tags:
            return

        if self._skip_element:
            if name == self._skip_element:
                self._skip_element = None

            return

        if name.lower() == 'display-name' and self._current_channel:
            if self._current_channel not in self._channels:
                self._channels[self._current_channel] = []
                
            self._channels[self._current_channel].append(self._last_data)
           # self._current_channel = None

        self._file.write('</{}>'.format(name.encode('utf8')))

    def start_element(self, name, attrs):
        if self._skip_element or name in self._ignore_tags:
            return

        attribs = {}
        l = ['']
        for i in range(0,len(attrs), 2):
            attribs[attrs[i].lower()] = attrs[i+1]
            l.append('{}="{}"'.format(attrs[i].encode('utf8'), escape(attrs[i+1]).encode('utf8')))
        
        if name.strip().lower() == 'channel':
            channel_id = attribs.get('id')
            if channel_id:
                self._current_channel = channel_id
                #self._channel_ids.append(channel_id)

        self._file.write('<{}{}>'.format(name.encode('utf8'), ' '.join(l)))

def merge_epgs(epgs, output_dir):
    log.debug('Merging {} EPGs...'.format(len(epgs)))

    merged_path = os.path.join(output_dir, '.iptv_merge_epg')

    with open(merged_path, 'wb') as outfile:
        outfile.write('<?xml version="1.0" encoding="utf-8" ?><tv generator-info-name="{}">'.format(ADDON_ID))

        parser = Parser(outfile)

        for epg in epgs:
            file_path = os.path.join(output_dir, '.iptv_merge_tmp')
            remove_file(file_path)
            process_file(epg, METHOD_EPG, file_path)

            log.debug('Processing: {}'.format(epg.path))
            parser.parse(file_path)

            remove_file(file_path)

        outfile.write('</tv>')

    log.debug('Merging EPGs Done')

    save_epg_channels(parser.channels)

    return merged_path

def run_merge(types):
    output_dir = xbmc.translatePath(settings.get('output_dir', '').strip() or ADDON_PROFILE)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    database.connect()

    try:
        if Source.PLAYLIST in types:
            playlists     = list(Source.select().where(Source.item_type == Source.PLAYLIST, Source.enabled == True).order_by(Source.order.asc()))
            playlist_path = merge_playlists(playlists, output_dir)

            shutil.move(playlist_path, os.path.join(output_dir, PLAYLIST_FILE_NAME))
        
        if Source.EPG in types:
            epgs         = list(Source.select().where(Source.item_type == Source.EPG, Source.enabled == True).order_by(Source.order.asc()))
            epg_path     = merge_epgs(epgs, output_dir)

            shutil.move(epg_path, os.path.join(output_dir, EPG_FILE_NAME))
    finally:
        database.close()

def start():
    restart_queued = False

    while not monitor.waitForAbort(2):
        forced = ADDON_DEV or xbmc.getInfoLabel('Skin.String({})'.format(ADDON_ID)) == FORCE_RUN_FLAG

        if forced or (settings.getBool('auto_merge', True) and time.time() - userdata.get('last_run', 0) > settings.getInt('reload_time_mins', 10) * 60):
            xbmc.executebuiltin('Skin.SetString({},{})'.format(ADDON_ID, FORCE_RUN_FLAG))
            
            try:
                run_merge([Source.PLAYLIST, Source.EPG])
            except Exception as e:
                result = False
                log.exception(e)
            else:
                result = True

            userdata.set('last_run', int(time.time()))
            xbmc.executebuiltin('Skin.SetString({},)'.format(ADDON_ID))

            if result:
                restart_queued = True

                if forced:
                    gui.notification(_.MERGE_COMPLETE)

            elif forced:
                gui.exception()

        if restart_queued and (forced or (settings.getBool('restart_pvr', False) and not xbmc.getCondVisibility('Pvr.IsPlayingTv') and not xbmc.getCondVisibility('Pvr.IsPlayingRadio'))):
            restart_queued = False

            xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":false}}}}'.format(IPTV_SIMPLE_ID))
            monitor.waitForAbort(2)
            xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":true}}}}'.format(IPTV_SIMPLE_ID))

        if ADDON_DEV:
            break