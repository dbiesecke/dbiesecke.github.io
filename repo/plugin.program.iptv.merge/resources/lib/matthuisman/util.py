import os
import time
import hashlib
import shutil
import platform
import struct

import xbmc, xbmcaddon

from .language import _
from .constants import ADDON_ID, ADDON_NAME, ADDON_PROFILE
from .log import log
from .exceptions import Error 
from . import gui

def remove_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except:
        return False
    else:
        return True

def hash_6(value, default=None):
    if not value:
        return default

    h = hashlib.md5(str(value))
    return h.digest().encode('base64')[:6]

def md5sum(filepath):
    if not os.path.exists(filepath):
        return None

    return hashlib.md5(open(filepath,'rb').read()).hexdigest()

def get_kodi_version():
    try:
        return int(xbmc.getInfoLabel("System.BuildVersion").split('.')[0])
    except:
        return 0

def process_brightcove(data):
    if type(data) != dict:
        try:
            msg = data[0].get('message', data[0]['error_code'])
        except KeyError:
            msg = _.NO_ERROR_MSG

        raise Error(_(_.NO_BRIGHTCOVE_SRC, error=msg))

    sources = []

    for source in data.get('sources', []):
        if not source.get('src'):
            continue

        # HLS
        if source.get('type') == 'application/x-mpegURL' and 'key_systems' not in source:
            sources.append({'source': source, 'type': 'hls', 'order_1': 1, 'order_2': int(source.get('ext_x_version', 0))})

        # MP4
        elif source.get('container') == 'MP4' and 'key_systems' not in source:
            sources.append({'source': source, 'type': 'mp4', 'order_1': 2, 'order_2': int(source.get('avg_bitrate', 0))})

        # Widevine
        elif source.get('type') == 'application/dash+xml' and 'com.widevine.alpha' in source.get('key_systems', ''):
            sources.append({'source': source, 'type': 'widevine', 'order_1': 3, 'order_2': 0})

        elif source.get('type') == 'application/vnd.apple.mpegurl' and 'key_systems' not in source:
            sources.append({'source': source, 'type': 'hls', 'order_1': 1, 'order_2': 0})

    if not sources:
        raise Error(_.NO_BRIGHTCOVE_SRC)

    sources = sorted(sources, key = lambda x: (x['order_1'], -x['order_2']))
    source = sources[0]

    from . import plugin, inputstream

    if source['type'] == 'mp4':
        return plugin.Item(
            path = source['source']['src'],
            art = False,
        )
    elif source['type'] == 'hls':
        return plugin.Item(
            path = source['source']['src'],
            inputstream = inputstream.HLS(),
            art = False,
        )
    elif source['type'] == 'widevine':
        return plugin.Item(
            path = source['source']['src'],
            inputstream = inputstream.Widevine(license_key=source['source']['key_systems']['com.widevine.alpha']['license_url']),
            art = False,
        )
    else:
        raise Error(_.NO_BRIGHTCOVE_SRC)

def migrate(new_addon_id, copy_userdata=True):
    def get_new_addon():
        try:
            return xbmcaddon.Addon(new_addon_id)
        except:
            return None

    if get_new_addon():
        return gui.ok(_(_.MIGRATE_OK, old_addon_id=ADDON_ID))

    if not gui.yes_no(_(_.CONFIRM_MIGRATE, new_addon_id=new_addon_id)):
        return

    xbmc.executebuiltin('InstallAddon({})'.format(new_addon_id), True)
    xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":true}}}}'.format(new_addon_id))

    dst_addon = get_new_addon()
    if not dst_addon:
        return

    if copy_userdata:
        dst_profile = xbmc.translatePath(dst_addon.getAddonInfo('profile')).decode("utf-8")

        if os.path.exists(dst_profile):
            shutil.rmtree(dst_profile)

        xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":false}}}}'.format(ADDON_ID))
        xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":false}}}}'.format(new_addon_id))

        shutil.copytree(ADDON_PROFILE, dst_profile)

        xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":true}}}}'.format(new_addon_id))

    gui.ok(_(_.MIGRATE_OK, old_addon_id=ADDON_ID))

def get_system_arch():
    if xbmc.getCondVisibility('System.Platform.UWP') or '4n2hpmxwrvr6p' in xbmc.translatePath('special://xbmc/'):
        system = 'UWP'
    elif xbmc.getCondVisibility('System.Platform.Android'):
        system = 'Android'
    elif xbmc.getCondVisibility('System.Platform.IOS'):
        system = 'IOS'
    else:
        system = platform.system()
    
    if system == 'Windows':
        arch = platform.architecture()[0]
    else:
        try:
            arch = platform.machine()
        except:
            arch = ''

    #64bit kernel with 32bit userland
    if ('aarch64' in arch or 'arm64' in arch) and (struct.calcsize("P") * 8) == 32:
        arch = 'armv7'

    elif 'arm' in arch:
        if 'v6' in arch:
            arch = 'armv6'
        else:
            arch = 'armv7'
            
    elif arch == 'i686':
        arch = 'i386'

    return system, arch