# provider info
NAME = "Soccerstreams100"
KEY = "soccerstreams100"

# page info
ROOT_URL = "https://my.soccerstreams100.tv/"
EVENT_URL = "https://streams100.net/event/"

if __name__ == "__main__":
    import sys
    import os
    import json

    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))
else:
    import xbmc
    from xbmcplugin import (
        addDirectoryItem,
        addDirectoryItems,
        endOfDirectory,
    )
    from xbmcgui import (
        ListItem,
    )

try:
    from router import PLUGIN, path_for_provider
    from helpers import http_get, header_random_agent, log
    from sources import url_to_source
except Exception as e:
    log(e)

import urllib
from bs4 import BeautifulSoup 

@PLUGIN.route(path_for_provider(KEY))
def root():
    def itemMaker(event):
        li = ListItem("[%s] %s - %s" % (
            event.get("category", "XY"),
            event.get("name", "UNKNOWN"),
            event.get("date", "Xyz")
        ))
        li.setArt({'thumb': event.get("thumb", None),
                'fanart': event.get("fanart", None)})
        return li
    events = get_all_events()
    items = list(map(lambda e: (PLUGIN.url_for(event, key=e["key"]), itemMaker(e), True), events))
    addDirectoryItems(PLUGIN.handle, items)
    endOfDirectory(PLUGIN.handle)

@PLUGIN.route("%s/events/<key>" % path_for_provider(KEY))
def event(key):
    def itemMaker(source, fn):
        li = ListItem("[%s][%s] %s (%s)" % (
            source.get("quality", "XY"),
            source.get("lang", "Xyz"),
            source.get("channel", "UNKNOWN"),
            fn.NAME,
        ))
        return li
    sources = get_all_sources(key)
    sources_dec = []
    for s in sources:
        source_fn = url_to_source(s["url"])
        sources_dec.append({"el": s, "fn": source_fn})
    items = list(map(lambda s: (PLUGIN.url_for(s["fn"].root,
                                            url=urllib.quote(s["el"]["url"].encode('utf8'), safe='')),
                                itemMaker(s["el"], s["fn"]), True), sources_dec))
    if (len(sources) == 0):
        li = ListItem("No playable sources found")
        addDirectoryItem(PLUGIN.handle, "", li)
    addDirectoryItems(PLUGIN.handle, items)
    endOfDirectory(PLUGIN.handle)

def get_all_sources(key):
    headers = header_random_agent()
    headers.update({"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
    url = "%s%s/" % (EVENT_URL, key)
    html = http_get(url, headers = headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    rows = soup.find_all("tr")
    if len(rows) == 0:
        return []
    all = []
    for r in rows:
        try:
            columns = r.find_all("td")
            if (len(columns) == 3):
                streamer = columns[0].getText().strip()
                quality = columns[2].string
                channel = columns[1]
                channel_name = channel.string
                url = channel.find("a").get("href")
                all.append({
                    "streamer": streamer,
                    "channel": channel_name,
                    "url": url
                })
            else:
                streamer = columns[0].getText().strip()
                quality = columns[1].string
                channel = columns[2]
                channel_name = channel.string
                url = channel.find("a").get("href")
                lang = columns[5].string
                all.append({
                    "streamer": streamer,
                    "quality": quality,
                    "channel": channel_name,
                    "lang": lang,
                    "url": url
                })
        except:
            pass
    return all

def safe_string_strip(o):
    if o and o.string:
        return o.string.strip()
    return ""

def get_all_events():
    html = http_get(ROOT_URL)
    soup = BeautifulSoup(html.text, 'html.parser')
    articles = soup.find_all("article")
    all = []
    for a in articles:
        title = a.find(rel="bookmark")
        name = title.string.strip()
        thumb = a.find("img").get("src")
        url = title.get("href")
        category = safe_string_strip(a.find(rel="category tag"))
        date = safe_string_strip(a.find(class_="post-date"))
        all.append({
            "name": name,
            "category": category,
            "date": date,
            "thumb": thumb,
            "url": url,
            "key": url.strip("/").split("/")[-1]
        })
    return all

def get_all_events_fake():
    return [{
            "name": "Sampdoria vs Napoli",
            "category": "Serie A",
            "date": "February 3, 2020 ",
            "thumb": "https://www.sofascore.com/images/team-logo/football_2675.png",
            "url": "https://streams100.net/event/sampdoria-vs-napoli-match-preview/",
            "key": "sampdoria-vs-napoli-match-preview"
    }]

if __name__ == "__main__":
    def test_get_all_events():
        r = get_all_events()
        print(r)

    def test_get_all_sources():
        r = get_all_sources("atletico-madrid-vs-liverpool-match-preview/")
        print(json.dumps(r))

    test_get_all_sources()
