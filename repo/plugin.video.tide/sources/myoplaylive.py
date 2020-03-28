"""
myoplay.live

method 1:
search for iframe https://angelthump.com/{id}/embed
m3u8 = https://video-cdn.angelthump.com/hls/{id}.m3u8

method 2:
search for iframe.contains "embed"
xyzembed common
"""

NAME = "myoplay.live"
KEY = "myoplaylive"
BASE = "myoplay.live"
M3U8_URL = "https://video-cdn.angelthump.com/hls/%s.m3u8"

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

import re
import urllib
from bs4 import BeautifulSoup

def can_handle(url):
    p_url = parse_url(url)
    return p_url.netloc == BASE

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    ref_url = urllib.unquote(url).decode('utf8')
    urls = get_urls(ref_url)
    add_items(urls, ref_url, PLUGIN)

def get_urls(url):
    p_url = parse_url(url)
    headers = header_random_agent()
    html = http_get(url, headers=headers)
    soup = BeautifulSoup(html.text, "html.parser")
    angel = re.search(r"angelthump.com/(.*?)/embed", html.text)
    headers.update({
        "Referer": url,
        "Origin": url,
    })
    if angel:
        angel_id = angel.group(1)
        return [M3U8_URL % angel_id]
    else:
        xyz = soup.find(allowfullscreen="true")
        xyz_url = "%s:%s" % (p_url.scheme, xyz.get("src"))
        html = http_get(xyz_url, headers=headers)
        return xyzembed(html.text)

# modification of wstream algo
def xyzembed(html):
    eval_f = re.search(r"<script>(eval.*?)</script>", html, re.MULTILINE | re.DOTALL).group(1)
    f = re.search(r"eval\((.*)\)", eval_f, re.MULTILINE | re.DOTALL).group(1)
    p = re.search(r"bestfit\|(.*)\|parentId", f).group(1).split('|')
    m3u8_url = "%s://%s.%s.%s:%s/%s/%s.%s?s=%s&e=%s" % (
        p[4], p[5], p[6], p[7], p[8], p[2], p[9], p[11], p[0], p[-1]
    )
    return m3u8_url

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("https://myoplay.live/oplive/")
    test_can_handle("https://myoplay.live/oplive/")
