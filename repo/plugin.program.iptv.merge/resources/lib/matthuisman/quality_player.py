from threading import Thread
from urlparse import urlparse

import xbmc
import json

from . import userdata, gui, router, inputstream, router
from .constants import ADDON_DEV
from .language import _
from .constants import QUALITY_ASK, QUALITY_BEST, QUALITY_CUSTOM, QUALITY_PASS, QUALITY_LOWEST, DEFAULT_QUALITY, ROUTE_QUALITY
from .log import log
from .exceptions import Error
from .parser import M3U8, MPD

PROXY_FILE = xbmc.translatePath('special://temp/proxy_playlist.m3u8')

def select_quality(qualities=None, is_settings=False):
    options = []

    if is_settings:
        options.append([QUALITY_ASK, _.QUALITY_ASK])

    options.append([QUALITY_BEST, _.QUALITY_BEST])
    options.extend(qualities or [[QUALITY_CUSTOM, _.QUALITY_CUSTOM]])
    options.append([QUALITY_LOWEST, _.QUALITY_LOWEST])
    options.append([QUALITY_PASS, _.QUALITY_PASSTHROUGH])

    values = [x[0] for x in options]
    labels = [x[1] for x in options]

    if is_settings:
        current = userdata.get('quality', DEFAULT_QUALITY)
    else:
        current = userdata.get('last_quality')

    default = 0
    if current:
        try:
            default = values.index(current)
        except:
            if not qualities:
                default = values.index(QUALITY_CUSTOM) if current > 0 else 0
            else:
                default = values.index(qualities[-1][0])

                for quality in qualities:
                    if quality[0] <= current:
                        default = values.index(quality[0])
                        break
                
    index = gui.select(_.SELECT_QUALITY, labels, preselect=default)
    if index < 0:
        return None

    value = values[index]
    label = labels[index]

    if value == QUALITY_CUSTOM:
        value = gui.numeric(_.QUALITY_CUSTOM_INPUT, default=current if current > 0 else '')
        if not value:
            return None

        value = int(value)
        label = _(_.QUALITY_BITRATE, bandwidth=float(value)/1000000, resolution='', fps='').strip()

    if is_settings:
        userdata.set('quality', value)
        gui.notification(_(_.QUALITY_SET, label=label))
    else:
        userdata.set('last_quality', value)

    return value

@router.route(ROUTE_QUALITY)
def _select_quality(**kwargs):
    select_quality(is_settings=True)

def reset_thread(reset_func):
    log.debug('Settings Reset Thread: STARTED')

    monitor    = xbmc.Monitor()
    player     = xbmc.Player()
    sleep_time = 100#ms

    #wait upto 3 seconds for playback to start
    count = 0
    while not monitor.abortRequested():
        if player.isPlaying():
            break

        if count > 3*(1000/sleep_time):
            break

        count += 1
        xbmc.sleep(sleep_time)

    #wait upto 30 seconds for playback to start
    count = 0
    while not monitor.abortRequested():
        if not player.isPlaying() or player.getTime() > 0:
            break

        if count > 30*(1000/sleep_time):
            break

        count += 1
        xbmc.sleep(sleep_time)

    reset_func()

    log.debug('Settings Reset Thread: DONE')

def get_gui_settings(keys):
    settings = {}

    for key in keys:
        try:
            value = json.loads(xbmc.executeJSONRPC('{{"jsonrpc":"2.0", "method":"Settings.GetSettingValue", "params":{{"setting":"{}"}}, "id":1}}'.format(key)))['result']['value']
            settings[key] = value
        except:
            pass
        
    return settings

def set_gui_settings(settings):
    for key in settings:
        xbmc.executeJSONRPC('{{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{{"setting":"{}", "value":{}}}, "id":1}}'.format(key, settings[key]))

def set_settings(min_bandwidth, max_bandwidth, is_ia=False):
    reset_func = None

    if is_ia:
        new_ia_settings = {
            'MINBANDWIDTH':        min_bandwidth,
            'MAXBANDWIDTH':        max_bandwidth,
            'IGNOREDISPLAY':       'true',
            'STREAMSELECTION':     '0',
            'MEDIATYPE':           '0',
            'MAXRESOLUTION':       '0',
            'MAXRESOLUTIONSECURE': '0',
        }

        current_ia_settings = inputstream.get_settings(new_ia_settings.keys())
        if new_ia_settings != current_ia_settings:
            inputstream.set_settings(new_ia_settings)
            reset_func = lambda: inputstream.set_settings(current_ia_settings)
    else:
        new_gui_settings = {
            'network.bandwidth': int(max_bandwidth/1000),
        }

        current_gui_settings = get_gui_settings(new_gui_settings.keys())
        if new_gui_settings != current_gui_settings:
            set_gui_settings(new_gui_settings)
            reset_func = lambda: set_gui_settings(current_gui_settings)

    if reset_func:
        thread = Thread(target=reset_thread, args=(reset_func,))
        thread.daemon = True
        thread.start()

def parse(item, quality=None):
    if quality is None:
        quality = userdata.get('quality', DEFAULT_QUALITY)
    else:
        quality = int(quality)

    if quality == QUALITY_PASS:
        return

    url   = item.path.split('|')[0]
    parse = urlparse(url.lower())
    
    if 'http' not in parse.scheme:
        return

    parser = None
    if item.inputstream and item.inputstream.check():
        is_ia = True
        if item.inputstream.manifest_type == 'mpd':
            parser = MPD()
        elif item.inputstream.manifest_type == 'hls':
            parser = M3U8()
    else:
        is_ia = False
        if parse.path.endswith('.m3u') or parse.path.endswith('.m3u8'):
            parser = M3U8()
            item.mimetype = 'application/vnd.apple.mpegurl'

    if not parser:
        return

    from .session import Session

    playlist_url = item.path.split('|')[0]

    try:
        resp = Session().get(playlist_url, headers=item.headers, cookies=item.cookies)
    except Exception as e:
        log.exception(e)
        result = False
    else:
        result = resp.ok

    if not result:
        return

    parser.parse(resp.text)
    qualities = parser.qualities()
    if len(qualities) < 2:
        return

    if quality == QUALITY_ASK:
        quality = select_quality(qualities)

    if not quality:
        return False

    elif quality == QUALITY_PASS:
        return

    min_bandwidth, max_bandwidth = parser.bandwidth_range(quality)
    set_settings(min_bandwidth, max_bandwidth, is_ia)