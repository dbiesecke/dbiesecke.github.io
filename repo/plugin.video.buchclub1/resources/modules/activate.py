# -*- coding: utf-8 -*-

from resources.lib import kodiutils
from resources.lib import kodilogging
import io
import os
import sys
import time
import urllib
import logging
import xbmcaddon
import xbmcgui
import xbmc
import shutil
from resources.lib import zfile as zipfile


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))


class Canceled(Exception):
    pass


class MyProgressDialog():
    def __init__(self, process):
        self.dp = xbmcgui.DialogProgress()
        self.dp.create("PsycoTV", process, '', '')

    def __call__(self, block_num, block_size, total_size):
        if self.dp.iscanceled():
            self.dp.close()
            raise Canceled
        percent = (block_num * block_size * 100) / total_size
        if percent < total_size:
            self.dp.update(percent)
        else:
            self.dp.close()


def read(response, progress_dialog):
    data = b""
    total_size = response.info().getheader('Content-Length').strip()
    total_size = int(total_size)
    bytes_so_far = 0
    chunk_size = 1024 * 1024
    reader = lambda: response.read(chunk_size)
    for index, chunk in enumerate(iter(reader, b"")):
        data += chunk
        progress_dialog(index, chunk_size, total_size)
    return data


def extract():
    url = xbmc.translatePath(os.path.join('special://home/userdata/activate.zip'))
    addon_folder = xbmc.translatePath(os.path.join('special://', 'home'))
    with zipfile.ZipFile(url, 'r') as zip_ref: zip_ref.extractall(addon_folder)
    return True


def get_packages():
        addon_name = ADDON.getAddonInfo('name')
        url = xbmc.translatePath(os.path.join('special://home/userdata/activate.zip'))
        addon_folder = xbmc.translatePath(os.path.join('special://', 'home'))
        if extract():
            dialog = xbmcgui.Dialog()
            dialog.ok('PsycoTV Pro', 'PsycoTV Pro wurde erfolgreich aktiviert. Die App wird nun geschlossen. Bitte die App erneut öffnen.')
            os._exit(0)
        
    