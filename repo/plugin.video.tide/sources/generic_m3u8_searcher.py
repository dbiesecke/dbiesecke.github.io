"""
Searches for all .m3u8 urls in the page and returns them.
Not very sophisticated, eh?
"""

NAME = "GenericM3U8Searcher"
KEY = "genericm3u8searcher"

if __name__ == "__main__":
    import sys
    import os
    import json
    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent, log
    from common import add_headers, add_items, parse_url
except Exception as e:
    print(e)

import urllib
import re
from bs4 import BeautifulSoup 

def can_handle(url):
    return False

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    ref_url = urllib.unquote(url).decode('utf8')
    urls = get_urls(ref_url)
    add_items(urls, ref_url, PLUGIN)

def get_urls(url):
    headers = header_random_agent()
    parsed_url = parse_url(url)
    html = http_get(url, headers=headers)
    urls = search(html.text)
    formatted = []
    for u in urls:
        if u.startswith("//"):
            formatted.append("%s:%s" % (parsed_url.scheme, u))
        else:
            formatted.append(u)
    no_duplicates = list(dict.fromkeys(formatted))
    return no_duplicates

def search(text):
    return re.findall(r'(?:https?:)?//.*?\.m3u8', text)

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    test("https://videojs.github.io/videojs-contrib-hls/")
