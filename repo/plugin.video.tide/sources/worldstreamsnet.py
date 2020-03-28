"""
worldstreams.net

method:
first iframe -> first iframe -> beautify -> m3u8
"""

NAME = "worldstreams.net"
KEY = "worldstreamsnet"
BASE = "wwww.worldstreams.net"

if __name__ == "__main__":
    import sys
    import os
    import json
    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent, log
    from common import add_headers, add_items, parse_url, wstreamto
except Exception as e:
    print(e)

import urllib
import base64
import re
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
    headers = header_random_agent()
    cookies = {}
    p_url = parse_url(url)
    html = http_get(url, headers=headers)
    cookies.update(html.cookies)
    soup = BeautifulSoup(html.text, 'html.parser')
    f_iframe_1_url = soup.find("iframe").get("src")
    headers.update({"Referer": url})
    html = http_get(f_iframe_1_url, headers=headers, cookies=cookies)
    cookies.update(html.cookies)
    soup = BeautifulSoup(html.text, 'html.parser')
    headers.update({"Referer": f_iframe_1_url})
    f_iframe_2_url = soup.find("iframe").get("src")
    html = http_get(f_iframe_2_url, headers=headers)
    return [wstreamto(html.text)]

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("http://wwww.worldstreams.net/p/athletic-bilbao-vs-barcelona.html")
    test_can_handle("http://wwww.worldstreams.net/p/athletic-bilbao-vs-barcelona.html")
