import os
import platform
import re
import shutil
import time

import xbmc, xbmcaddon

from . import gui, settings
from .log import log
from .constants import IA_ADDON_ID, IA_VERSION_KEY, IA_HLS_MIN_VER, IA_MPD_MIN_VER, IA_MODULES_URL, IA_CHECK_EVERY
from .language import _
from .util import get_kodi_version, md5sum, remove_file, get_system_arch, hash_6
from .exceptions import InputStreamError

class InputstreamItem(object):
    manifest_type = ''
    license_type  = ''
    license_key   = ''
    mimetype      = ''
    checked       = None

    def do_check(self):
        return False

    def check(self):
        if self.checked is None:
            self.checked = self.do_check()
            
        return self.checked

class HLS(InputstreamItem):
    manifest_type = 'hls'
    mimetype      = 'application/vnd.apple.mpegurl'

    def do_check(self):
        return settings.getBool('use_ia_hls', False) and supports_hls()

class MPD(InputstreamItem):
    manifest_type = 'mpd'
    mimetype      = 'application/dash+xml'

    def do_check(self):
        return supports_mpd()

class Playready(InputstreamItem):
    manifest_type = 'ism'
    license_type  = 'com.microsoft.playready'
    mimetype      = 'application/vnd.ms-sstr+xml'

    def do_check(self):
        return supports_playready()

class Widevine(InputstreamItem):
    manifest_type = 'mpd'
    license_type  = 'com.widevine.alpha'
    mimetype      = 'application/dash+xml'

    def __init__(self, license_key=None, content_type='application/octet-stream', challenge='R{SSM}', response=''):
        self.license_key  = license_key
        self.content_type = content_type
        self.challenge    = challenge
        self.response     = response

    def do_check(self):
        return install_widevine()

def get_ia_addon(required=False, install=True):
    try:
        if install:
            xbmc.executebuiltin('InstallAddon({})'.format(IA_ADDON_ID), True)
            xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":true}}}}'.format(IA_ADDON_ID))

        return xbmcaddon.Addon(IA_ADDON_ID)
    except:
        pass

    if required:
        raise InputStreamError(_.IA_NOT_FOUND)

    return None

def set_settings(settings):
    addon = get_ia_addon(install=False)
    if not addon:
        return

    log.debug('IA Set Settings: {}'.format(settings))

    for key in settings:
        addon.setSetting(key, str(settings[key]))

def get_settings(keys):
    addon = get_ia_addon(install=False)
    if not addon:
        return None

    settings = {}
    for key in keys:
        settings[key] = addon.getSetting(key)

    return settings

def open_settings():
    ia_addon = get_ia_addon(required=True)
    ia_addon.openSettings()

def supports_hls():
    ia_addon = get_ia_addon()
    return bool(ia_addon and int(ia_addon.getAddonInfo('version')[0]) >= IA_HLS_MIN_VER)

def supports_mpd():
    ia_addon = get_ia_addon()
    return bool(ia_addon and int(ia_addon.getAddonInfo('version')[0]) >= IA_MPD_MIN_VER)

def supports_playready():
    ia_addon = get_ia_addon()
    return bool(ia_addon and get_kodi_version() > 17 and xbmc.getCondVisibility('system.platform.android'))

def install_widevine(reinstall=False):
    ia_addon     = get_ia_addon(required=True)
    system, arch = get_system_arch()
    kodi_version = get_kodi_version()
    DST_FILES    = {
        'Linux':   'libwidevinecdm.so',
        'Darwin':  'libwidevinecdm.dylib',
        'Windows': 'widevinecdm.dll',
    }

    if kodi_version < 18:
        raise InputStreamError(_(_.IA_KODI18_REQUIRED, system=system))

    elif system == 'Android':
        return True

    elif system == 'UWP':
        raise InputStreamError(_.IA_UWP_ERROR)

    elif 'aarch64' in arch or 'arm64' in arch:
        raise InputStreamError(_.IA_AARCH64_ERROR)
    
    elif system not in DST_FILES:
        raise InputStreamError(_(_.IA_NOT_SUPPORTED, system=system, arch=arch, kodi_version=kodi_version))

    last_check   = int(ia_addon.getSetting('_last_check') or 0)
    decryptpath  = xbmc.translatePath(ia_addon.getSetting('DECRYPTERPATH')).decode("utf-8")
    wv_path      = os.path.join(decryptpath, DST_FILES[system])
    installed    = md5sum(wv_path)

    if not installed:
        reinstall = True

    if not reinstall and time.time() - last_check < IA_CHECK_EVERY:
        return True

    ## DO INSTALL ##
    ia_addon.setSetting('_last_check', str(int(time.time())))

    from .session import Session

    r = Session().get(IA_MODULES_URL)
    if r.status_code != 200:
        raise InputStreamError(_(_.ERROR_DOWNLOADING_FILE, filename=IA_MODULES_URL.split('/')[-1]))

    widevine     = r.json()['widevine']
    wv_versions  = widevine['platforms'].get(system + arch, [])
    latest       = wv_versions[0]
    latest_known = ia_addon.getSetting('_latest_md5')
    ia_addon.setSetting('_latest_md5', latest['md5'])

    if not wv_versions:
        raise InputStreamError(_(_.IA_NOT_SUPPORTED, system=system, arch=arch, kodi_version=kodi_version))

    if not reinstall and (installed == latest['md5'] or latest['md5'] == latest_known):
        return True

    current = None
    for wv in wv_versions:
        if wv['md5'] == installed:
            current = wv
            wv['label'] = _(_.WV_INSTALLED, version=wv['ver'])
        else:
            wv['label'] = wv['ver']

    if installed and not current:
        wv_versions.append({
            'ver': installed[:6],
            'label': _(_.WV_UNKNOWN, version=installed[:6]),
        })

    latest['label'] = _(_.WV_LATEST, label=latest['label'])
    labels = [x['label'] for x in wv_versions]

    index = gui.select(_.SELECT_WV_VERSION, options=labels)
    if index < 0:
        return False

    selected = wv_versions[index]

    if 'src' in selected:
        url = widevine['base_url'] + selected['src']
        if not _download(url, wv_path, selected['md5']):
            return False

    if selected != latest:
        message = _.WV_NOT_LATEST
    else:
        message = _.IA_WV_INSTALL_OK
    
    gui.ok(_(message, version=selected['ver']))

    return True

def _download(url, dst_path, md5=None):
    dir_path = os.path.dirname(dst_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    filename   = url.split('/')[-1]
    downloaded = 0

    if os.path.exists(dst_path):
        if md5 and md5sum(dst_path) == md5:
            log.debug('MD5 of local file {} same. Skipping download'.format(filename))
            return True
        else:
            remove_file(dst_path)
            
    from .session import Session

    with gui.progress(_(_.IA_DOWNLOADING_FILE, url=filename), heading=_.IA_WIDEVINE_DRM) as progress:
        resp = Session().get(url, stream=True)
        if resp.status_code != 200:
            raise InputStreamError(_(_.ERROR_DOWNLOADING_FILE, filename=filename))

        total_length = float(resp.headers.get('content-length', 1))

        with open(dst_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=settings.getInt('chunksize', 4096)):
                f.write(chunk)
                downloaded += len(chunk)
                percent = int(downloaded*100/total_length)

                if progress.iscanceled():
                    progress.close()
                    resp.close()

                progress.update(percent)

    if progress.iscanceled():
        remove_file(dst_path)            
        return False

    checksum = md5sum(dst_path)
    if checksum != md5:
        remove_file(dst_path)
        raise InputStreamError(_(_.MD5_MISMATCH, filename=filename, local_md5=checksum, remote_md5=md5))
    
    return True