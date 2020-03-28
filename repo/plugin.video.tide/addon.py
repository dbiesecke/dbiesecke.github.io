# -*- coding: utf-8 -*-
"""tide main file"""

import xbmc
import xbmcaddon

from xbmcgui import (
    ListItem,
    Dialog,
    DialogProgress,
)

from xbmcplugin import (
    addDirectoryItem,
    addDirectoryItems,
    addSortMethod,
    endOfDirectory,
    setContent,
    setResolvedUrl,
    SORT_METHOD_LABEL_IGNORE_THE
)

from router import PLUGIN
from providers import all_providers

# initialize routing
ADDON = xbmcaddon.Addon('plugin.video.tide')

@PLUGIN.route("/")
def index():
    """Start page of addon"""
    items = list(map(lambda p: (PLUGIN.url_for(p.root), ListItem(p.NAME), True), all_providers))
    addDirectoryItems(PLUGIN.handle, items)
    endOfDirectory(PLUGIN.handle)

if __name__ == '__main__':
    PLUGIN.run()
