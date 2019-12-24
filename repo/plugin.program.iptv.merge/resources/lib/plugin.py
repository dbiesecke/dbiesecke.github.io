import os
import json

import xbmc, xbmcaddon, xbmcgui

from matthuisman import plugin, settings, gui, userdata
from matthuisman.constants import ADDON_ID, ADDON_PROFILE
from matthuisman.exceptions import PluginError

from difflib import SequenceMatcher

from .language import _
from .models import Source, Channels, load_epg_channels
from .constants import FORCE_RUN_FLAG, IPTV_SIMPLE_ID, PLAYLIST_FILE_NAME, EPG_FILE_NAME

@plugin.route('')
def home(**kwargs):
    folder = plugin.Folder()

    folder.add_item(
        label = _(_.PLAYLISTS, _bold=True), 
        path  = plugin.url_for(playlists),
    )

    folder.add_item(
        label = _(_.EPGS, _bold=True), 
        path  = plugin.url_for(epgs),
    )

    folder.add_item(
        label = _(_.CHANNEL_MANAGER, _bold=True), 
        path  = plugin.url_for(channel_manager),
    )

    folder.add_item(
        label = _.MERGE_NOW, 
        path  = plugin.url_for(merge),
    )

    folder.add_item(label=_.SETTINGS, path=plugin.url_for(plugin.ROUTE_SETTINGS))

    return folder

@plugin.route()
def channel_manager(sort=None, **kwargs):
    folder = plugin.Folder(title=_.CHANNEL_MANAGER)

    if not sort:
        folder.add_item(
            label = _(_.TV, _bold=True), 
            path  = plugin.url_for(channel_manager, sort='tv'),
        )

        folder.add_item(
            label = _(_.RADIO, _bold=True),
            path  = plugin.url_for(channel_manager, sort='radio'),
        )
        
        return folder

    epg_channels = load_epg_channels()

    for channel in Channels().channel_list():
        id       = channel.pop('_id')
        hidden   = channel.pop('_hidden', False)
        url      = channel.pop('_url', '')
        name     = channel.pop('_name', '') or url
        source   = channel.pop('_source', '')
        chno     = channel.get('tvg-chno')
        group    = channel.get('group-title', '')
        radio    = channel.get('radio', False)
        modified = channel.get('_modified', False)
        tvg_id   = channel.get('tvg-id')
        added    = channel.get('_added', False)

        if (sort == 'tv' and radio) or (sort == 'radio' and not radio):
            continue

        if chno != None:
            name = _(_.CHANNEL_WITH_NUMBER, number=chno, label=name)

        if group:
            name = _(_.CHANNEL_WITH_GROUP, group=group, label=name)

        if hidden:
            name = _(_.HIDDEN, label=name, _color='red')

        if tvg_id not in epg_channels:
            name = _(_.NO_EPG, label=name)

        context = []
        
        context.append((_.RENAME_CHANNEL, "XBMC.RunPlugin({})".format(plugin.url_for(edit_channel, id=id, key='_name'))))
        context.append((_.SET_CHANNEL_NUMBER, "XBMC.RunPlugin({})".format(plugin.url_for(edit_channel, id=id, key='tvg-chno'))))
        context.append((_.SET_CHANNEL_LOGO, "XBMC.RunPlugin({})".format(plugin.url_for(edit_channel, id=id, key='tvg-logo'))))
        context.append((_.SET_CHANNEL_GROUP, "XBMC.RunPlugin({})".format(plugin.url_for(edit_channel, id=id, key='group-title'))))
        context.append((_.SET_CHANNEL_ID, "XBMC.RunPlugin({})".format(plugin.url_for(edit_channel, id=id, key='tvg-id'))))

        if hidden:
            context.append((_.SHOW_CHANNEL, "XBMC.RunPlugin({})".format(plugin.url_for(edit_channel, id=id, key='_hidden'))))
        else:
            context.append((_.HIDE_CHANNEL, "XBMC.RunPlugin({})".format(plugin.url_for(edit_channel, id=id, key='_hidden'))))

        context.append((_.PLAY, "XBMC.PlayMedia({})".format(url)))

        if modified:
            name = _(name, _color='blue')
            context.append((_.DELETE_CHANNEL if added else _.RESET_CHANNEL, "XBMC.RunPlugin({})".format(plugin.url_for(reset_channel, id=id))))

        folder.add_item(
            label     = name,
            art       = {'thumb': channel.get('tvg-logo')},
            info      = {'plot': url},
            path      = plugin.url_for(edit_channel, id=id, key='tvg-chno'),
            context   = context,
            is_folder = True,
        )

    folder.add_item(
        label = _.ADD_CHANNEL,
        path  = plugin.url_for(add_channel, sort=sort),
    )

    return folder

@plugin.route()
def add_channel(sort=None, **kwargs):
    url = gui.input(_.CHANNEL_PATH)
    if url:
        channels = Channels()
        channels.add(url, is_radio=sort=='radio')
        gui.refresh()

@plugin.route()
def reset_channel(id, **kwargs):
    channels = Channels()
    channels.clear_overrides(id)
    gui.refresh()

def get_tvg_id(channel):
    epg_channels = load_epg_channels()

    channel_epgs = []
    for row in Channels().channel_list():
        tvg_id  = row.get('tvg-id')
        if tvg_id:
            channel_epgs.append(tvg_id)

    tvg_id     = channel.get('tvg-id', '')
    name       = channel.get('_name').lower().strip()
    best_match = None
    values     = []
    labels     = []

    for key in sorted(epg_channels.keys()):
        values.append(key)
        names = ' / '.join(epg_channels[key]).strip()
        label = _(_.EPG_ID_LABEL, epg_id=key, names=names)

        if key == tvg_id:
            label = _(_.CURRENT_EPG, label=label)
        elif key in channel_epgs:
            label = _(_.ASSIGNED_EPG, label=label)

        labels.append(label)

        for value in epg_channels[key]:
            ratio = SequenceMatcher(None, name, value.lower().strip()).quick_ratio()
            if not best_match or ratio > best_match[0]:
                best_match = [ratio, key]

    labels.append(_.CUSTOM_EPG)
    values.append(None)

    if best_match and best_match[1] != tvg_id:
        index = values.index(best_match[1])
        labels[index] = _(_.BEST_MATCH_EPG, label=labels[index])

    if tvg_id:
        try:
            default = values.index(tvg_id)
        except:
            default = len(values) - 1
    else:
        if best_match:
            default = values.index(best_match[1])
        else:
            default = 0

    index = gui.select(_.SET_CHANNEL_ID, labels, preselect=default)
    if index < 0:
        return None

    value = values[index]
    if value == None:
        value = gui.input(_.CUSTOM_EPG, default=tvg_id)
        
    return value

@plugin.route()
def edit_channel(id, key, **kwargs):
    channels = Channels()
    channel  = channels.get(id)

    if key == '_hidden':
        value = not channel['_hidden']
    elif key == '_name':
        default = channel['_name']
        value = gui.input(_.RENAME_CHANNEL, default=default)
        if not value or value == default:
            return
    elif key == 'tvg-chno':
        default = channel.get('tvg-chno', '')
        value = gui.numeric(_.SET_CHANNEL_NUMBER, default=default)
        if not value or value == default:
            return
        value = int(value)
    elif key == 'tvg-logo':
        default = channel.get('tvg-logo', '')
        value = gui.input(_.SET_CHANNEL_LOGO, default=default)
        if not value or value == default:
            return
    elif key == 'group-title':
        default = channel.get('group-title', '')
        value = gui.input(_.SET_CHANNEL_GROUP, default=default)
        if not value or value == default:
            return
    elif key == 'tvg-id':
        value = get_tvg_id(channel)
        if not value:
            return
    else:
        return

    channels.set_override(id, key, value)
    gui.refresh()

@plugin.route()
def setup(**kwargs):
    try:
        xbmc.executebuiltin('InstallAddon({})'.format(IPTV_SIMPLE_ID), True)
        xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":true}}}}'.format(IPTV_SIMPLE_ID))
        addon = xbmcaddon.Addon(IPTV_SIMPLE_ID)
    except:
        raise PluginError(_.NO_IPTV_SIMPLE)

    xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":false}}}}'.format(IPTV_SIMPLE_ID))

    output_dir    = xbmc.translatePath(settings.get('output_dir', '').strip() or ADDON_PROFILE)
    playlist_path = os.path.join(output_dir, PLAYLIST_FILE_NAME)
    epg_path      = os.path.join(output_dir, EPG_FILE_NAME)

    addon.setSetting('m3uPathType', '0')
    addon.setSetting('m3uPath', playlist_path)

    addon.setSetting('epgPathType', '0')
    addon.setSetting('epgPath', epg_path)
    
    settings.setBool('restart_pvr', True)

    xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":true}}}}'.format(IPTV_SIMPLE_ID))
    
    xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"epg.futuredaystodisplay", "value":7}, "id":1}')
    xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.backendchannelorder", "value":true}, "id":1}')
    xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.usebackendchannelnumbers", "value":true}, "id":1}')
    xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.syncchannelgroups", "value":true}, "id":1}')
    xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"epg.ignoredbforclient", "value":true}, "id":1}')
    #xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.preselectplayingchannel", "value":true}, "id":1}')

    gui.ok(_.SETUP_COMPLETE)


@plugin.route()
def toggle_source(id, **kwargs):
    source = Source.get_by_id(id)
    source.enabled = not source.enabled
    source.save()

    gui.refresh()

@plugin.route()
def shift_source(id, shift, **kwargs):
    shift  = int(shift)
    source = Source.get_by_id(id)

    Source.update(order = Source.order - shift).where(Source.order == source.order + shift).execute()
    source.order += shift
    source.save()

    gui.refresh()

def _process_sources(sources):
    items = []

    for source in sources:
        label = source.label()

        if not source.enabled:
            label = _(_.DISABLED, label=label, _color='red')

        item = plugin.Item(
            label = label,
            path  = plugin.url_for(edit_source, id=source.id),
        )

        if source.order > 0:
            item.context.append((_.MOVE_UP, 'XBMC.RunPlugin({})'.format(plugin.url_for(shift_source, id=source.id, shift=-1))))

        if source.order < len(sources) - 1:
            item.context.append((_.MOVE_DOWN, 'XBMC.RunPlugin({})'.format(plugin.url_for(shift_source, id=source.id, shift=1))))

        item.context.append((_.EDIT_SOURCE, 'XBMC.RunPlugin({})'.format(plugin.url_for(edit_source, id=source.id))))

        if source.enabled:
            item.context.append((_.DISABLE_SOURCE, 'XBMC.RunPlugin({})'.format(plugin.url_for(toggle_source, id=source.id))))
        else:
            item.context.append((_.ENABLE_SOURCE, 'XBMC.RunPlugin({})'.format(plugin.url_for(toggle_source, id=source.id))))

        item.context.append((_.DELETE_SOURCE, 'XBMC.RunPlugin({})'.format(plugin.url_for(delete_source, id=source.id))))

        items.append(item)

    return items

@plugin.route()
def playlists(**kwargs):
    folder  = plugin.Folder(title=_.PLAYLISTS)
    sources = Source.select().where(Source.item_type == Source.PLAYLIST).order_by(Source.order.asc())

    items = _process_sources(sources)
    folder.add_items(items)

    folder.add_item(
        label = _(_.ADD_PLAYLIST, _bold=len(items) == 0), 
        path  = plugin.url_for(edit_source, type=Source.PLAYLIST, order=len(items)),
    )

    return folder

@plugin.route()
def epgs(**kwargs):
    folder  = plugin.Folder(title=_.EPGS)
    sources = Source.select().where(Source.item_type == Source.EPG).order_by(Source.order.asc())

    items = _process_sources(sources)
    folder.add_items(items)

    folder.add_item(
        label = _(_.ADD_EPG, _bold=len(items) == 0), 
        path  = plugin.url_for(edit_source, type=Source.EPG, order=len(items)),
    )

    return folder

@plugin.route()
def delete_source(id, **kwargs):
    source = Source.get_by_id(id)
    
    if gui.yes_no(_.CONFIRM_DELETE_SOURCE):
        source.delete_instance()
        Source.update(order = Source.order - 1).where(Source.order > source.order).execute()
        gui.refresh()

@plugin.route()
def edit_source(id=None, type=None, order=0, **kwargs):
    if id:
        source = Source.get_by_id(id)
    else:
        source = Source(item_type=type, order=order)

    if source.wizard():
        source.save()
        gui.refresh()

@plugin.route()
def merge(**kwargs):
    if xbmc.getInfoLabel('Skin.String({})'.format(ADDON_ID)) == FORCE_RUN_FLAG:
        raise PluginError(_.MERGE_IN_PROGRESS)

    xbmc.executebuiltin('Skin.SetString({},{})'.format(ADDON_ID, FORCE_RUN_FLAG))
    gui.notification(_.MERGE_STARTED)

@plugin.route()
def import_sources(**kwargs):
    file_path = xbmcgui.Dialog().browseSingle(1, _.SELECT_IMPORT_FILE, "", mask='.iptv_merge')
    if not file_path:
        return

    with open(file_path) as f:
        data = json.load(f)

    Source.truncate()

    count = 0
    for row in data:
        try:
            source = Source(**row)
            source.save()
        except:
            continue
        else:
            count += 1

    gui.notification(_(_.SOURCES_IMPORTED, count=count))

@plugin.route()
def export_sources(**kwargs):
    folder = xbmcgui.Dialog().browseSingle(3, _.SELECT_EXPORT_FOLDER, "")
    if not folder:
        return

    folder = xbmc.translatePath(folder)
    path   = os.path.join(folder, 'export.iptv_merge')

    data = []
    for source in Source.select():
        data.append({
            'item_type': source.item_type, 
            'path_type': source.path_type, 
            'path'     : source.path, 
            'file_type': source.file_type,
            'order'    : source.order,
            'enabled'  : source.enabled,
        })

    with open(path, 'w') as outfile:
        json.dump(data, outfile)

    gui.notification(_(_.SOURCES_EXPORTED, count=len(data)))

@plugin.route()
def proxy_merge(type=None, **kwargs):
    from .service import run_merge

    output_dir    = xbmc.translatePath(settings.get('output_dir', '').strip() or ADDON_PROFILE)
    playlist_path = os.path.join(output_dir, PLAYLIST_FILE_NAME)
    epg_path      = os.path.join(output_dir, EPG_FILE_NAME)

    if type == 'epg':
        run_merge([Source.EPG])
        return plugin.Item(path=epg_path)

    elif type == 'playlist':
        run_merge([Source.PLAYLIST])
        return plugin.Item(path=playlist_path)

    else:
        run_merge([Source.EPG, Source.PLAYLIST])
        return plugin.Item(path=output_dir)