import os
import json

import xbmc, xbmcgui, xbmcaddon

from matthuisman import peewee, database, gui, settings
from matthuisman.exceptions import Error
from matthuisman.constants import ADDON_PROFILE
from matthuisman.util import hash_6
from matthuisman.log import log

from .constants import MERGE_SETTING_FILE, METHOD_PLAYLIST, METHOD_EPG, MERGE_VERSION, CHANNELS_FILE, OVERRIDE_FILE, EPG_CHANNELS_FILE
from .language import _

def save_epg_channels(channels):
    with open(os.path.join(ADDON_PROFILE, EPG_CHANNELS_FILE), 'wb') as f:
        f.write(json.dumps(channels, ensure_ascii=False, encoding='utf8').encode('utf8'))

def load_epg_channels():
    try:
        with open(os.path.join(ADDON_PROFILE, EPG_CHANNELS_FILE), 'rb') as f:
            return json.load(f, encoding='utf8')
    except:
        return {}

class Channels(object):
    def __init__(self):
        self._load()

    def _load(self):
        try:
            with open(os.path.join(ADDON_PROFILE, CHANNELS_FILE), 'rb') as f:
                self._channels = json.load(f, encoding='utf8')
        except:
            log.debug('Failed to load channels file')
            self._channels = []

        try:
            with open(os.path.join(ADDON_PROFILE, OVERRIDE_FILE), 'rb') as f:
                self._overrides = json.load(f, encoding='utf8')
        except:
            log.debug('Failed to load overrides file')
            self._overrides = {}

        for key in self._overrides:
            if self._overrides[key].get('_added'):
                self._channels.append({'_url': key, '_name': '', '_source': ''})

        last_chn_no = 0
        for channel in self._channels:
            channel['_id']       = channel.get('tvg-id') or channel['_url']
            channel['_hidden']   = settings.getBool('default_hidden', False)
            channel['_modified'] = False

            try:
                channel['tvg-chno'] = int(channel['tvg-chno'])
                last_chn_no = channel['tvg-chno']
            except:
                last_chn_no += 1
                channel['tvg-chno'] = last_chn_no

            overrides = None
            
            if 'tvg-id' in channel:
                overrides = self._overrides.get(channel['tvg-id'])

            if not overrides:
                overrides = self._overrides.get(channel['_url'])

            if overrides:
                channel['_modified'] = True
                channel.update(overrides)

    @classmethod
    def set_channels(cls, channels):
        with open(os.path.join(ADDON_PROFILE, CHANNELS_FILE), 'wb') as f:
            f.write(json.dumps(channels, ensure_ascii=False, encoding='utf8').encode('utf8'))

    def add(self, url, is_radio=False):
        data = {'_added': True}
        if is_radio:
            data['radio'] = 'true'
        
        if url in self._overrides:
            raise Error(_.URL_TAKEN)

        self._overrides[url] = data
        self.save_overrides()

    def set_override(self, id, key, value):
        id = id.decode('utf8')

        if id not in self._overrides:
            self._overrides[id] = {}

        self._overrides[id][key] = value
        self.save_overrides()

    def clear_overrides(self, id):
        id = id.decode('utf8')

        self._overrides.pop(id, None)
        self.save_overrides()

    def save_overrides(self):
        with open(os.path.join(ADDON_PROFILE, OVERRIDE_FILE), 'wb') as f:
            f.write(json.dumps(self._overrides, ensure_ascii=False, encoding='utf8').encode('utf8'))

        self._load()

    def get(self, id):
        id = id.decode('utf8')

        for channel in self._channels:
            if channel['_id'] == id:
                return channel

        raise Error('Unable to find!')

    def playlist(self):
        return sorted(self._channels, key=lambda c: (c.get('group-title'), c.get('radio'), c['tvg-chno'], c['_name']))

    def channel_list(self):
        return sorted(self._channels, key=lambda c: (c['tvg-chno'], c['_name']))

class Source(database.Model):
    PLAYLIST = 0
    EPG = 1

    TYPE_REMOTE = 0
    TYPE_LOCAL  = 1
    TYPE_ADDON  = 2

    FILE_STANDARD = 0
    FILE_GZIP     = 1

    item_type     = peewee.IntegerField()
    path_type     = peewee.IntegerField()
    path          = peewee.TextField()
    file_type     = peewee.IntegerField(default=FILE_STANDARD)

    order         = peewee.IntegerField(default=0)
    enabled       = peewee.BooleanField(default=True)

    class Meta:
        indexes = (
            (('item_type', 'path'), True),
        )

    def label(self):
        if self.path_type == self.TYPE_ADDON:
            try:
                return '{} ({})'.format(xbmcaddon.Addon(self.path).getAddonInfo('name'), self.path)
            except:
                return self.path
        else:
            return self.path

    def wizard(self):
        types   = [self.TYPE_REMOTE, self.TYPE_LOCAL, self.TYPE_ADDON]
        options = [_.REMOTE_PATH, _.LOCAL_PATH, _.ADDON_SOURCE]
        default = self.path_type or self.TYPE_REMOTE

        index   = gui.select(_.CHOOSE, options, preselect=types.index(default))
        if index < 0:
            return False

        self.path_type = types[index]

        if self.path_type == self.TYPE_ADDON:
            addons  = self._get_merge_addons()
            if not addons:
                raise Error(_.NO_ADDONS)

            ids     = [x['id'] for x in addons]
            options = [x['name'] for x in addons]

            try:
                default = ids.index(self.path)
            except ValueError:
                default = 0

            index = gui.select(_.CHOOSE, options, preselect=default)
            if index < 0:
                return False

            self.path      = ids[index]
            self.file_type = self.FILE_STANDARD
            
            return True

        elif self.path_type == self.TYPE_REMOTE:
            self.path = gui.input(_.URL, default=self.path)
        elif self.path_type == self.TYPE_LOCAL:
            self.path = xbmcgui.Dialog().browseSingle(1, _.BROWSE_FILE, self.path or '', '')

        if not self.path:
            return False

        types   = [self.FILE_STANDARD, self.FILE_GZIP]
        options = [_.STANDARD_FILE, _.GZIPPED_FILE]
        default = self.file_type or (self.FILE_GZIP if self.path.endswith('.gz') else self.FILE_STANDARD)

        index   = gui.select(_.CHOOSE, options, preselect=types.index(default))
        if index < 0:
            return False

        self.file_type = types[index]

        return True

    def _get_merge_addons(self):
        addons = []

        payload = {
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'Addons.GetAddons',
            'params': {'installed': True, 'enabled': True, 'type': 'xbmc.python.pluginsource'},
        }

        response = xbmc.executeJSONRPC(json.dumps(payload))
        data     = json.loads(response)

        for row in data['result']['addons']:
            addon      = xbmcaddon.Addon(row['addonid'])
            addon_path = xbmc.translatePath(addon.getAddonInfo('path')).decode("utf-8")
            merge_path = os.path.join(addon_path, MERGE_SETTING_FILE)
            
            if not os.path.exists(merge_path):
                continue

            with open(merge_path) as f:
                data = json.load(f)
            
            min_req_version = data.get('version')
            if not min_req_version or min_req_version > MERGE_VERSION:
                continue

            if int(self.item_type) == self.PLAYLIST and METHOD_PLAYLIST not in data:
                continue

            if int(self.item_type) == self.EPG and METHOD_EPG not in data:
                continue

            addons.append({'name': addon.getAddonInfo('name'), 'id': addon.getAddonInfo('id')})

        return addons

database.tables.extend([Source])