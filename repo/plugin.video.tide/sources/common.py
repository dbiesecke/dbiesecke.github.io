import urllib
import re
try:
    from urllib.parse import urlparse, urljoin
except ImportError:
     from urlparse import urlparse, urljoin
try:
    import xbmc
    from xbmcplugin import (
        addDirectoryItem,
        addDirectoryItems,
        endOfDirectory,
    )
    from xbmcgui import (
        ListItem,
    )
except:
    pass

def add_headers(url, referer, origin = None):
    if not origin:
        origin = referer
    return "%s|referer=%s|origin=%s" % (url, referer, origin)

def add_items(urls, ref_url, PLUGIN):
    no_duplicates = list(dict.fromkeys(urls))
    for i in range(len(no_duplicates)):
        title = "Source %d" % i
        li = ListItem(title)
        li.setInfo('video', {'title': title,
                                    'mediatype': 'video'})
        m3u8_url = urllib.quote(urls[i], safe="%/:=&?~#+!$,;'@()*[]")
        addDirectoryItem(PLUGIN.handle, add_headers(m3u8_url, ref_url), li)
    if (len(urls) == 0):
        li = ListItem("No playable sources found")
        addDirectoryItem(PLUGIN.handle, "", li)
    endOfDirectory(PLUGIN.handle)

def parse_url(url):
    return urlparse(url)

def join_url(a, b):
    return urljoin(a, b)

def wstreamto(html):
    eval_f = re.search(r"<script>(eval.*?)</script>", html, re.MULTILINE | re.DOTALL).group(1)
    f = re.search(r"eval\((.*)\)", eval_f, re.MULTILINE | re.DOTALL).group(1)
    p = re.search(r"(\d{10}.*)\|setAttribute", f).group(1).split('|')
    m3u8_url = "%s://%s.%s.%s:%s/%s/%s.%s?s=%s&e=%s" % (
        p[4], p[5], p[6], p[7], p[8], p[2], p[9], p[11], p[-1], p[0]
    )
    return m3u8_url
